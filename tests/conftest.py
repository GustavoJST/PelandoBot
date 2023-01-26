import pytest
from pelandobot.scraper.promotion_scraper import PromotionScraper
from pelandobot.app.bot import start_bot
from pelandobot.tgbot.utils.database import sync_db
from multiprocessing import Process


# This function cleans the database of uncessary data.
# It's used in a fixture to clean the database before and after tests.
def clean_db_for_tests():
    # Cleans all promotions control related tables.
    if sync_db.redis.exists("unsent.promotions.id"):
        promotions_id = sync_db.redis.lrange("unsent.promotions.id", 0, -1)
        for id in promotions_id:
            sync_db.redis.delete(f"promotion.{id}.info")
            sync_db.redis.delete(f"promotion.{id}.tags")
    sync_db.redis.delete("promotions.id")
    sync_db.redis.delete("unsent.promotions.id")

    # Reset /tags state for active users.
    users_id = sync_db.redis.smembers("active.chats.id")
    for user_id in users_id:
        sync_db.redis.delete(f"state.{user_id}")


@pytest.fixture(scope="session")
def scraper():
    yield PromotionScraper()


@pytest.fixture(scope="function")
def prepare_db():
    clean_db_for_tests()
    yield
    clean_db_for_tests()


@pytest.fixture(scope="module")
def prepare_bot_connection():
    bot_runner = Process(target=start_bot)
    bot_runner.start()
    yield
    bot_runner.kill()


@pytest.fixture(scope="session")
def bot_connection():
    bot_runner = Process(target=start_bot)
    bot_runner.start()
    yield
    bot_runner.kill()
