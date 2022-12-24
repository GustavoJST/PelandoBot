import pytest
from promotion_scraper import PromotionScraper
from tgbot.utils.database import sync_db


@pytest.fixture(scope="function")
def scraper():
    return PromotionScraper()
    
    
""" @pytest.fixture(scope="function")
def mock_data():
    return {"id": "45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
            "title": "[AME R$2960]Smart TV 65\" Crystal UHD 4K Samsung 65BU8000 (R$ 962,00 cashback pela ame)",
            "price": "3699.99",
            "url": "https://www.pelando.com.br/d/45c2ba07-0e40-41a4-b7c1-5ec63ce39791/",
            "image": "https://api.pelando.com.br/media/f55db4fb-074c-4a31-b102-eaa3a982e88b?v=2",
            "tags": {'65', 'samsung', 'smart', 'cashback', 'pela', 'tv', 'ame', '4k', 
                        '96200', '65bu8000', '2960', 'crystal', 'uhd'}} """
 

    


