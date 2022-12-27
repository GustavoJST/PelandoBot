import pytest
from pelandobot.promotion_scraper import PromotionScraper


@pytest.fixture(scope="function")
def scraper():
    return PromotionScraper()
