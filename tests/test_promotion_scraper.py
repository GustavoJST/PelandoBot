import pytest
import json
import requests
from pelandobot.scraper.promotion_scraper import PromotionScraper
from pelandobot.tgbot.utils.database import sync_db
from tests.variables_and_parameters import (
    TEST_POPULATE_DB_WITH_PROMOTIONS_EXPECTED as expected_promotions_id,
    TEST_GET_PROMOTION_TAGS_REGEX_PARAMS,
    TEST_GET_PROMOTION_INFO_PARAMS,
)


def test_get_params_com_first_query_true(scraper: PromotionScraper):
    target_params = {
        "operationName": "RecentOffersQuery",
        "variables": '{"limit":50}',
        "extensions": '{"persistedQuery":'
        '{"version":1,'
        '"sha256Hash":"38c288ba7f66706afcb33f3206b00229c0a86fb140bad72a262603e12b422802"}}',
    }
    params = scraper.get_params()
    assert params == target_params


def test_get_params_com_first_query_false(scraper: PromotionScraper):
    target_params = {
        "operationName": "RecentOffersQuery",
        "variables": '{"limit":25}',
        "extensions": '{"persistedQuery":'
        '{"version":1,'
        '"sha256Hash":"38c288ba7f66706afcb33f3206b00229c0a86fb140bad72a262603e12b422802"}}',
    }
    scraper.first_query = False
    params = scraper.get_params()
    assert params == target_params


def test_check_request_status_code(scraper: PromotionScraper):
    with requests.Session() as session:
        params = scraper.get_params()
        data, status_code = scraper.make_request(session, params)
        assert status_code == 200


def test_populate_db_with_promotions(scraper: PromotionScraper, prepare_db):

    with open("./tests/mock_data.json", "r") as json_file:
        mock_data = json.load(json_file)
    scraper.populate_db_with_promotions(mock_data)
    db_ids = sync_db.redis.lrange("promotions.id", 0, -1)
    assert db_ids == expected_promotions_id


@pytest.mark.parametrize(
    "test_input, expected_tags",
    TEST_GET_PROMOTION_TAGS_REGEX_PARAMS,
)
def test_get_promotion_tags_regex(scraper: PromotionScraper, test_input, expected_tags):
    tags = scraper.get_promotion_tags(test_input)
    assert tags == expected_tags


@pytest.mark.parametrize("test_input, expected_promotion_info", TEST_GET_PROMOTION_INFO_PARAMS)
def test_get_promotion_info(test_input, expected_promotion_info):
    scraper = PromotionScraper()
    promotion_info = scraper.get_promotion_info(test_input)
    assert promotion_info == expected_promotion_info


@pytest.fixture(scope="function")
def mock_data():
    return {
        "id": "45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
        "title": '[AME R$2960]Smart TV 65" Crystal UHD 4K Samsung 65BU8000 '
        "(R$ 962,00 cashback pela ame)",
        "price": "3699.99",
        "url": "https://www.pelando.com.br/d/45c2ba07-0e40-41a4-b7c1-5ec63ce39791",
        "image": "https://api.pelando.com.br/media/f55db4fb-074c-4a31-b102-eaa3a982e88b?v=2",
        "tags": {
            "65",
            "samsung",
            "smart",
            "cashback",
            "pela",
            "tv",
            "ame",
            "4k",
            "96200",
            "65bu8000",
            "2960",
            "crystal",
            "uhd",
        },
    }


def test_push_promotions_to_db_exists_unsent_promotions(
    scraper: PromotionScraper, mock_data, prepare_db
):
    scraper.push_promotion_to_db(mock_data)
    assert sync_db.redis.exists("unsent.promotions.id") == 1


def test_push_promotions_to_db_exists_promotion_info_tags(
    scraper: PromotionScraper, mock_data, prepare_db
):
    scraper.push_promotion_to_db(mock_data)
    tags = sync_db.redis.smembers(f"promotion.{mock_data['id']}.tags")
    assert tags == mock_data["tags"]


def test_push_promotions_to_db_exists_promotion_info(scraper: PromotionScraper, mock_data, prepare_db):
    scraper.push_promotion_to_db(mock_data)
    promotion_info = sync_db.redis.hgetall(f"promotion.{mock_data['id']}.info")
    mock_data.pop("tags")
    mock_data.pop("id")
    assert promotion_info == mock_data
