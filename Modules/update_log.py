#!/usr/bin/python
# -*- coding: utf-8 -*-
# import threading
from datetime import datetime
# from init_logging import *
from Modules.get_latest_json import *
from Modules.get_location import *
from Modules.init_blinkt import green_led
from Modules.get_config import get_config

# read the config file
config = get_config()

THREADING_TIMER = config['THREADING_TIMER']


# get timestamp and build a human readable format
def get_timestamp():
    current_time = datetime.now()

    return current_time.isoformat()


def update_log():

    # threading.Timer(THREADING_TIMER, update_log).start()

    json_data = get_latest_json()

    timestamp = get_timestamp()

    temperature = json_data['currently']['temperature']

    sensor_temp_inside = json_data['currently']['sensor_temp_inside']
    sensor_temp_outside = json_data['currently']['sensor_temp_outside']

    rain_percentage_data = json_data['currently']['precipProbability']
    rain_percentage = rain_percentage_data * 100

    sensor_pressure_inside = json_data['currently']['sensor_pressure_inside']
    sensor_humidity_inside = json_data['currently']['sensor_humidity_inside']

    sensor_pressure_outside = json_data['currently']['sensor_pressure_outside']
    sensor_humidity_outside = json_data['currently']['sensor_humidity_outside']

    summary = json_data['currently']['summary'].encode('UTF-8')

    daily = json_data['daily']['data']
    forecast_today = daily[0]

    temp_range_today_min = int(forecast_today['temperatureMin'])
    temp_range_today_max = int(forecast_today['temperatureMax'])

    hourly_forecast = json_data['hourly']['summary']

    io_str = '{} bis {}°C - {}'.format(
        temp_range_today_min,
        temp_range_today_max,
        hourly_forecast.encode('UTF-8')
    )

    location_data = get_location()

    location = location_data['city']
    latitude = location_data['lat']  # geolocation data for the request url
    longitude = location_data['lon']  # geolocation data for the request url

    log_string = '[timestamp={}], [temp_api={}], [sensor_temp_inside={}], [sensor_temp_outside={}],' \
                 ' [rain_percentage={}], [sensor_pressure_inside={}], [sensor_humidity_inside={}],' \
                 ' [sensor_pressure_outside={}], [sensor_humidity_outside={}], [summary="{}"],' \
                 ' [next_weather_today="{}"], [latitude={}], [longitude={}], [location={}]'.format(
        timestamp,
        temperature,
        sensor_temp_inside,
        sensor_temp_outside,
        rain_percentage,
        sensor_pressure_inside,
        sensor_humidity_inside,
        sensor_pressure_outside,
        sensor_humidity_outside,
        summary,
        io_str,
        latitude,
        longitude,
        location
    )

    # write log_string to log file
    weather_logger.info(log_string)

    green_led()

    log_string = 'created log entry: {}'.format(log_string)

    print(log_string)
    debug_logger.debug(log_string)

if __name__ == '__main__':
    update_log()
