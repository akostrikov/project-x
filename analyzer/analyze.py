import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.point import Point

import ssl
import geopy.geocoders
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
geopy.geocoders.options.default_ssl_context = ctx


def parse_city(lat, lon):
    locator = Nominatim(user_agent="city_geocoder")
    coordinates = f"{lat}, {lon}"

    location = locator.reverse(coordinates)

    res = ''
    location_raw = location.raw["address"]
    if 'city' in location_raw:
        res = location_raw['city']
    if 'town' in location_raw:
        res = location_raw['town']
    if res == '':
        res = location_raw['display_name']

    return res

def analyze(data):
    vin = data["vin"]
    break_treshold = data['breakThreshold']
    tank_size = data['gasTankSize']

    data_points = data['data']
    prev_point = data_points[0]
    rest_points = []
    refuel_points = []
    resting_time = 0
    curr_rest_start = None
    refuel_state = False
    
    start_point = data_points[0]
    end_point = data_points[-1]
    start_city = parse_city(start_point['positionLat'], start_point['positionLong'])
    end_city   = parse_city(end_point['positionLat'], end_point['positionLong'])

    total_distance = 0
    total_rest_time = 0
    
    total_liters_percents = 0 
    for point in data_points[1:]:
        distance = int(point['odometer']) - int(prev_point['odometer'])
        rest_time = int(point['timestamp']) - int(prev_point['timestamp'])
        fuel_diff = int(point['fuelLevel']) - int(prev_point['fuelLevel'])
        if (fuel_diff < 0):
            total_liters_percents -= fuel_diff

        total_distance += distance
        
        if distance == 0:
            if resting_time == 0:
                curr_rest_start = prev_point['timestamp']
            resting_time += rest_time    

        if resting_time >= break_treshold and distance > 0:
            rest_points.append(
                {
                    "startTimestamp": curr_rest_start,
                    "endTimestamp": prev_point['timestamp'],
                    "positionLat": prev_point['positionLat'],
                    "positionLong": prev_point['positionLong']
                }
            )


        if resting_time and refuel_state and distance > 0:
            refuel_points.append(
                {
                    "startTimestamp": curr_rest_start,
                    "endTimestamp": prev_point['timestamp'],
                    "positionLat": prev_point['positionLat'],
                    "positionLong": prev_point['positionLong']
                }
            )
            refuel_state = False

        if distance > 0:
            total_rest_time += resting_time
            resting_time = 0

        if fuel_diff > 0:
            refuel_state = True

        prev_point = point

    total_liters = total_liters_percents / 100.0 * tank_size
    consumption = round(total_liters / total_distance * 100, 1)

    result = {
        'vin': vin,
        'departure': start_city,
        'destination': end_city,
        'refuelStops': refuel_points,
        'consumption': consumption,
        'breaks': rest_points
    }
    return result
