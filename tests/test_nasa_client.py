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


def test_get_curiosity_photos(earth_date):
    client = NasaClient()

    response = client.curiosity_photos(earth_date=earth_date)

    assert len(response) == 4