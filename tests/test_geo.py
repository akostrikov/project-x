import pytest

import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.point import Point
from geopy.distance import distance



def test_city_parser():
    locator = Nominatim(user_agent="myGeocoder")
    coordinates = "48.771990, 9.172787"

    location = locator.reverse(coordinates)
    city = location.raw["address"]["city"]

    assert city == "Stuttgart"

def test_distance_parser():
    start = Point(48.771990, 9.172787)
    end = Point(49.771990, 10.172787)
    assert distance(start, end).kilometers == pytest.approx(132, abs=1)
