import time
import requests
from tgbot.utils.database import sync_db

def get_promotions():
    first_query = True
    
    while True:
        time.sleep(3)
        url = "https://www.pelando.com.br/api/graphql"

        querystring = {"operationName":"RecentOffersQuery",
                    "variables":"{\"limit\":30}",
                    "extensions":"{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"38c288ba7f66706afcb33f3206b00229c0a86fb140bad72a262603e12b422802\"}}"}

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

        response = requests.request("GET", url, headers=headers, params=querystring)
        
        # Making GET requests to the URL rarely returns a persistedQuery error.
        # The code below adds a status check and restarts the loop if the status is not 200,
        # trying a new request in the next iteration.
        if response.status_code != 200:
            time.sleep(3)
            continue
        data = response.json()
        
        if first_query == True:
            if sync_db.redis.exists("promotions.id"):
                sync_db.redis.delete("promotions.id")
                
            # Populate the promotions_ids list with the latest promotions, as we only want new promotions from now on.
            for promotion in data["data"]["public"]["recentOffers"]["edges"]:
                sync_db.redis.rpush("promotions.id", promotion["id"])
            first_query = False   
        
        promotions_id = sync_db.redis.lrange("promotions.id", 0, -1)
        
        for promotion in data["data"]["public"]["recentOffers"]["edges"]:   
            if promotion["id"] in promotions_id:    
                continue
            # TODO: Talvez dê problema pois o número de ids guardada no banco de dados é o mesmo que 
            # o número de ids obtidas com o GET.
            sync_db.redis.lpush("promotions.id", promotion["id"])
            sync_db.redis.rpop("promotions.id")
            sync_db.redis.rpush("active.promotions.id", promotion["id"])
            
            # TODO: Os preços, as vezes saem como grátis embora tenham preço no site,
            # será q é devido a falta da utilização do async?
            title = promotion["title"]
            promotion_price = "Grátis" if promotion["price"] in [0, None] else f"R$ {float(promotion['price']):.2f}".replace('.', ',')
            promotion_url = f"https://www.pelando.com.br/d/{promotion['id']}"
            
            sync_db.redis.hset(f"promotion.{promotion['id']}.info", 
                               mapping={"title": title, 
                                        "price": promotion_price, 
                                        "url": promotion_url})


        