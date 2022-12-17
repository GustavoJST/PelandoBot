import aiohttp
import re
import asyncio
import timeit
import send_promotions
from tgbot.utils.database import sync_db
from multiprocessing import Process

async def get_promotions():
    first_query = True
    active_process = False
    
    # GET request headers generated by Insomnia.
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
            "Accept": "*/*",
            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, utf-8",
            "Referer": "https://www.pelando.com.br/recentes",
            "content-type": "application/json",
            "Alt-Used": "www.pelando.com.br",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        while True:
            await asyncio.sleep(8)
            # TODO: Remove later in cleanup
            # start = timeit.default_timer()
            
            # GET request params snippet generated by Insomnia.
            url = "https://www.pelando.com.br/api/graphql"

            if first_query == True:
                querystring = {"operationName":"RecentOffersQuery",
                            f"variables":"{\"limit\":50}",
                            "extensions":"{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"38c288ba7f66706afcb33f3206b00229c0a86fb140bad72a262603e12b422802\"}}"}
            else:
                querystring = {"operationName":"RecentOffersQuery",
                            "variables":"{\"limit\":25}",
                            "extensions":"{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"38c288ba7f66706afcb33f3206b00229c0a86fb140bad72a262603e12b422802\"}}"}
      
            async with session.get(url, params=querystring) as resp:
                data = await resp.json()
            
            # Making GET requests to the URL rarely returns a persistedQuery error.
            # The code below adds content check and restarts the loop if the content 
            # contains an error, trying a new request in the next iteration of the loop.
            try:
                test_response = data["data"]["public"]["recentOffers"]["edges"]
            except KeyError:
                await asyncio.sleep(2)
                continue

            if first_query == True:
                sync_db.redis.delete("promotions.id")
                    
                # Populate the promotions_ids list with the latest promotions, as we only want new promotions from now on.
                for promotion in data["data"]["public"]["recentOffers"]["edges"]:
                    sync_db.redis.rpush("promotions.id", promotion["id"])
                first_query = False   
            
            promotions_id = sync_db.redis.lrange("promotions.id", 0, -1)
            
            for promotion in data["data"]["public"]["recentOffers"]["edges"]:
                # Filters promotions that were already delivered or not approved by the website.
                if promotion["id"] in promotions_id or not promotion["timestamps"]["approvedAt"]:    
                    continue

                sync_db.redis.lpush("promotions.id", promotion["id"])
                sync_db.redis.rpop("promotions.id")
                sync_db.redis.lpush("unsent.promotions.id", promotion["id"])
                
                title = promotion["title"]
                promotion_price = "Grátis" if promotion["price"] in [0, None] else f"R$ {float(promotion['price']):.2f}".replace('.', ',')
                promotion_url = f"https://www.pelando.com.br/d/{promotion['id']}"
                promotion_image = promotion["image"]["original"]
                
                # Very rarely, no URL will be passed to the variable promotion_image
                # using the "original" keyword.
                if promotion_image is None:
                    promotion_image = promotion["image"]["large"]
                
                # First filter fixes cases like [text]128gb from becoming 'text128gb', 
                # as that would fuse two tags in one.
                # Instead, it becomes 'text 128gb'.
                # OBS: Both filter_1 and filter_2 could've been implemented using \W to match
                # all non-word characters, but the problem is that this filter it's too broad.
                # This implementation, albeit more dumber, allows for a more fine control.
                filter_1 = re.sub("[\[\]$%+*\(\):;?°{}®™=&\-|]", " ", title.lower())
                
                # filter_2 is for symbols that appear frequently in promotion titles.
                filter_2 = re.sub("[,\/\\.]", "", filter_1)
                
                # last filter deletes single character words/digits like "a","e","o", 1.
                promotion_tags = set(re.sub("(?i)(?<=\s|\,)\w(?=\s|\,)", "", filter_2).split(" "))
                promotion_tags.discard("")
                sync_db.redis.sadd(f"promotion.{promotion['id']}.tags", *promotion_tags)
                sync_db.redis.hset(f"promotion.{promotion['id']}.info", mapping={"title": title, 
                                                                        "price": promotion_price, 
                                                                        "url": promotion_url,
                                                                        "image": promotion_image})
                
            if sync_db.redis.exists("unsent.promotions.id"):      
                if active_process == False:
                    m_sender = Process(target=send_promotions.prepare_process)
                    m_sender.start()
                    active_process = True
                    await asyncio.sleep(1)
                    
                if not m_sender.is_alive() and sync_db.redis.exists("unsent.promotions.id"):
                    active_process = False
            
            # print(f"get_promotions - elapsed time = {timeit.default_timer() - start}")

        