import pytest
import json
from promotion_scraper import PromotionScraper
from tgbot.utils.database import sync_db
from bot import clean_db
from tests.testing_variables import TEST_POPULATE_DB_WITH_PROMOTIONS as expected_promotions_id


def test_get_params_com_first_query_true(scraper: PromotionScraper):
    target_params = {"operationName":"RecentOffersQuery",
                        "variables":"{\"limit\":50}",
                        "extensions":"{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"38c288ba7f66706afcb33f3206b00229c0a86fb140bad72a262603e12b422802\"}}"}
    params = scraper.get_params()
    assert params == target_params
    
    
def test_get_params_com_first_query_false(scraper: PromotionScraper):
    target_params = {"operationName":"RecentOffersQuery",
                        "variables":"{\"limit\":25}",
                        "extensions":"{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"38c288ba7f66706afcb33f3206b00229c0a86fb140bad72a262603e12b422802\"}}"}
    scraper.first_query = False
    params = scraper.get_params()
    assert params == target_params
    

def test_populate_db_with_promotions(scraper: PromotionScraper):
    with open("./tests/mock_data.json", "r") as json_file:
        mock_data = json.load(json_file)
    scraper.populate_db_with_promotions(mock_data)
    db_ids = sync_db.redis.lrange("promotions.id", 0, -1)
    assert db_ids == expected_promotions_id
    clean_db()
 

@pytest.mark.parametrize("test_input,expected_tags", [
    ("[App] Monitor Gamer Curvo Samsung Odyssey 27\" WQHD, 240Hz, 1ms, HDMI", 
     {'samsung', 'curvo', 'wqhd', 'hdmi', '27', '240hz', '1ms', 'app', 'odyssey', 'monitor', 'gamer'}),
    
    ("SSD Hikvision E3000, 512GB, M.2 2280, NVMe, Leitura 3476MB/s e Gravação 3137MB/s, HS-SSD-E3000/512G",
    {'e3000', '3476mbs', 'hikvision', 'hs', 'e3000512g', '3137mbs', 'gravação', 'ssd', '2280', 'nvme', '512gb', 'm2', 'leitura'}),
    
    ("[AME R$ 10,49 / AME SC R$ 7,34 ] - Livro - O milagre da manhã: O segredo para transformar sua vida",
    {'livro', 'segredo', 'vida', 'sc', 'milagre', 'sua', '1049', 'manhã', 'para', 'ame', '734', 'transformar', 'da'}),
    
    ("Cupom Insider de 20% OFF primeira compra!",
    {'cupom', '20', 'off', 'primeira', 'de', 'insider', 'compra'}),
    
    ("Comprar o Assassin's Creed® Odyssey - EDIÇÃO ULTIMATE | Xbox",
    {'creed', 'ultimate', 'xbox', 'comprar', 'odyssey', 'assassins', 'edição'}),
    
    ("[AME R$2960]Smart TV 65\" Crystal UHD 4K Samsung 65BU8000 (R$ 962,00 cashback pela ame)",
    {'cashback', '65bu8000', 'uhd', '2960', 'samsung', '65', '96200', 'smart', '4k', 'ame', 'tv', 'pela', 'crystal'}),
    
    ("Monitor Gamer Mancer Valak ZX240H, 27Pol., VA, FHD, 1ms, 240Hz, Freesync e G-Sync, HDMI/DP, MCR-VZX240H-BL01",
    {'vzx240h', '27pol', 'monitor', '1ms', 'gamer', 'mancer', '240hz', 'bl01', 'freesync', 'fhd', 'sync', 'va', 'hdmidp', 'valak', 'mcr', 'zx240h'}),
    
    ("[AME R$ 107 R$ SC 32 ] Piscina Inflável Fast Set 2.490 Litros - brink+",
    {'ame', '32', '2490', 'brink', 'set', 'piscina', 'fast', 'inflável', 'sc', '107', 'litros'}),
    
    ("Need for Speed™ Heat Edição Deluxe[PS4]",
    {'for', 'need', 'heat', 'edição', 'deluxe', 'speed', 'ps4'}),
    
    ("Compre 2 leve 3 Shampoo Anticaspa Head & Shoulders 400ml",
    {'head', 'shoulders', 'leve', 'anticaspa', 'compre', 'shampoo', '400ml'})
])
def test_get_promotion_tags_regex(scraper: PromotionScraper, test_input, expected_tags):
    tags = scraper.get_promotion_tags(test_input)
    assert tags == expected_tags
    
    
@pytest.mark.parametrize("test_input,expected_promotion_info", [
    ({"id": "45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
    "title": "[AME R$2960]Smart TV 65\" Crystal UHD 4K Samsung 65BU8000 (R$ 962,00 cashback pela ame)",
    "price": 3699.99,
    "image": {"original": "https://api.pelando.com.br/media/f55db4fb-074c-4a31-b102-eaa3a982e88b?v=2"}},
      
    {"id": "45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
    "title": "[AME R$2960]Smart TV 65\" Crystal UHD 4K Samsung 65BU8000 (R$ 962,00 cashback pela ame)",
    "price": "R$ 3699,99",
    "url": "https://www.pelando.com.br/d/45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
    "image": "https://api.pelando.com.br/media/f55db4fb-074c-4a31-b102-eaa3a982e88b?v=2",
    "tags": {'cashback', '65bu8000', 'uhd', '2960', 'samsung', '65', '96200', 'smart', '4k', 'ame', 'tv', 'pela', 'crystal'}}),
    
    
   ({"id": "215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
    "title": "Jogo Metro Last Light Redux - PC",
    "price": 0,
    "image": {"original": "https://api.pelando.com.br/media/ff95c1ec-f330-4457-8221-186c6616c697?v=2"}},
      
    {"id": "215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
    "title": "Jogo Metro Last Light Redux - PC",
    "price": "Grátis",
    "url": "https://www.pelando.com.br/d/215dfe1d-ed62-4a07-b8bf-71176d8b47fc",
    "image": "https://api.pelando.com.br/media/ff95c1ec-f330-4457-8221-186c6616c697?v=2",
    "tags": {'jogo', 'last', 'redux', 'metro', 'pc', 'light'}})
])
def test_get_promotion_info(test_input, expected_promotion_info):
    scraper = PromotionScraper()
    promotion_info = scraper.get_promotion_info(test_input)
    assert promotion_info == expected_promotion_info
    

@pytest.fixture(scope="function")
def mock_data():
    return {"id": "45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
                "title": "[AME R$2960]Smart TV 65\" Crystal UHD 4K Samsung 65BU8000 (R$ 962,00 cashback pela ame)",
                "price": "3699.99",
                "url": "https://www.pelando.com.br/d/45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
                "image": "https://api.pelando.com.br/media/f55db4fb-074c-4a31-b102-eaa3a982e88b?v=2",
                "tags": {'65', 'samsung', 'smart', 'cashback', 'pela', 'tv', 'ame', '4k', 
                         '96200', '65bu8000', '2960', 'crystal', 'uhd'}}  
    
    
def test_push_promotions_to_db_exists_unsent_promotions(scraper: PromotionScraper, mock_data):
    scraper.push_promotion_to_db(mock_data)
    assert sync_db.redis.exists("unsent.promotions.id") == True
    clean_db()
    
    
def test_push_promotions_to_db_exists_promotion_info_tags(scraper: PromotionScraper, mock_data):
    scraper.push_promotion_to_db(mock_data)
    tags = sync_db.redis.smembers(f"promotion.{mock_data['id']}.tags")
    assert tags == mock_data["tags"]
    clean_db()
    
    
def test_push_promotions_to_db_exists_promotion_info(scraper: PromotionScraper, mock_data):
    scraper.push_promotion_to_db(mock_data)
    promotion_info = sync_db.redis.hgetall(f"promotion.{mock_data['id']}.info")
    mock_data.pop("tags")
    mock_data.pop("id")
    assert promotion_info == mock_data
    clean_db()
    
    
def test_spawn_msender_process(scraper: PromotionScraper):
    m_sender = scraper.spawn_msender_process()
    assert m_sender != None
      