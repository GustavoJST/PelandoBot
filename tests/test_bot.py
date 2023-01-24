import requests
import pytest
from pelandobot.tgbot.utils.database import sync_db
from tests.variables_and_parameters import (
    TEST_CLEAN_DB_DELETE_PROMOTION_INFO_DATA as promo_mock_data,
    TEST_POPULATE_DB_WITH_PROMOTIONS_EXPECTED as mock_ids,
    TEST_WEBHOOK_MOCK_DATA as mock_json,
)
from pelandobot.bot import (
    clean_db,
    shutdown,
    app_setup,
    TOKEN,
    WEBHOOK_HOST,
    WEBHOOK_PORT,
    CHAT_TYPES,
)


def test_bot_chat_types():
    assert CHAT_TYPES == ["private", "group", "supergroup"]


def test_clean_db_delete_promotion_info(prepare_db):
    for promotion in promo_mock_data:
        sync_db.redis.lpush("unsent.promotions.id", promotion["id"])
        sync_db.redis.hset(
            f"promotion.{promotion['id']}.info",
            mapping={
                "title": promotion["title"],
                "price": promotion["price"],
                "url": promotion["url"],
                "image": promotion["image"],
            },
        )
    clean_db()
    for promotion_id in sync_db.redis.lrange("unsent.promotions.id", 0, -1):
        assert sync_db.redis.hgetall(f"promotion.{promotion_id}.info") is None


def test_clean_db_delete_promotion_tags(prepare_db):
    for promotion in promo_mock_data:
        sync_db.redis.lpush("unsent.promotions.id", promotion["id"])
        sync_db.redis.hset(
            f"promotion.{promotion['id']}.info",
            mapping={
                "title": promotion["title"],
                "price": promotion["price"],
                "url": promotion["url"],
                "image": promotion["image"],
            },
        )
    clean_db()
    for promotion_id in sync_db.redis.lrange("unsent.promotions.id", 0, -1):
        assert sync_db.redis.hgetall(f"promotion.{promotion_id}.tags") is None


def test_clean_db_delete_promotion_ids(prepare_db):
    sync_db.redis.lpush("promotions.id", *mock_ids)
    clean_db()
    assert sync_db.redis.lrange("promotions.id", 0, -1) == []


def test_clean_db_delete_unsent_promotion_ids(prepare_db):
    sync_db.redis.lpush("unsent.promotions.id", *mock_ids)
    clean_db()
    assert sync_db.redis.lrange("unsent.promotions.id", 0, -1) == []


@pytest.mark.asyncio
async def test_bot_webhook(bot_connection):
    url = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}/{TOKEN}/"
    response = requests.post(url, json=mock_json, verify="./webhook_cert.pem")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_bot_webhook_shutdown(bot_connection):
    await shutdown(await app_setup())
    url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
    response = requests.get(url).json()
    assert response["result"]["url"] == ""


# TODO: Adicionar mais testes do bot.py
