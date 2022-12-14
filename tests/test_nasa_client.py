import logging

import pytest

from fevo.nasa import NasaClient


@pytest.fixture
def earth_date():
    return "2015-06-03"


def test_client_with_api_key():
    client = NasaClient(api_key="test_key")

    assert isinstance(client, NasaClient)
    assert client.base_url == "https://api.nasa.gov"
    assert client.params.get("api_key") == "test_key"


def test_client_no_api_key():
    client = NasaClient()

    assert isinstance(client, NasaClient)
    assert client.base_url == "https://api.nasa.gov"
    assert client.params.get("api_key") == "DEMO_KEY"


def test_mars_rover_photos(earth_date):
    client = NasaClient()

    response, is_cached = client.mars_rover_photos(rover="curiosity", earth_date=earth_date)
    assert len(response) == 4


def test_get_curiosity_photos(earth_date):
    client = NasaClient()

    response, is_cached = client.curiosity_photos(earth_date=earth_date)
    assert len(response) == 4
    assert len(client.cache_strategy.cache.keys()) == 1


def test_get_curiosity_photos_with_limit(earth_date):
    for i in range(1, 4):
        client = NasaClient()
        response, is_cached = client.curiosity_photos(earth_date=earth_date, photo_limit=i)
        assert len(response) == i
        assert len(client.cache_strategy.cache.keys()) == 1


def test_cache_strategy(earth_date, caplog):
    caplog.set_level(logging.INFO)

    client = NasaClient()

    response, is_cached = client.curiosity_photos(earth_date=earth_date)
    assert len(response) == 4
    assert not is_cached

    second_response, is_cached = client.curiosity_photos(earth_date=earth_date)
    assert len(second_response) == 4
    assert is_cached
