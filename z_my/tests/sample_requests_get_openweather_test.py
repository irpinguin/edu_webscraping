import pytest
from edu.sample_requests_get_openweather import get_weather, get_token


CITY = 'Irkutsk'
CITY_WRONG = 'qwer'


def test_get_weather_city():
    """ test for the right city """
    assert get_weather(CITY, get_token())


def test_get_weather_city_neg():
    """ test for the wrong city """
    assert get_weather(CITY_WRONG, get_token()) is None


def test_get_weather_auth():
    """auth with token"""
    assert get_weather(CITY, get_token())


def test_get_weather_auth_neg():
    """auth with empty token"""
    assert get_weather(CITY, '') is None


if __name__ == '__main__':
    pytest.test_get_weather_auth()
