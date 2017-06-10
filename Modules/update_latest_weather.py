#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests

from get_latest_json import *
from init_blinkt import *
from init_io import *

# read the config file
config = get_config()

# set the configs
FORECAST_IO_KEY = config['FORECAST_IO_KEY']
THREADING_TIMER = config['THREADING_TIMER']

# parameter for the request url
FORECAST_URL = 'https://api.forecast.io/forecast/'  # endpoint for the API

LATITUDE = config['LATITUDE']
LONGITUDE = config['LONGITUDE']

options = '?lang=de&units=si&exclude=flags'  # some options, see details in API documentation


# build and return the request url
def get_request_url():
    request_url = FORECAST_URL + FORECAST_IO_KEY + '/' + str(LATITUDE) + ',' + str(LONGITUDE) + options  # build it

    log_string('build request url: {}'.format(request_url))

    return request_url


def update_latest_weather():

    # threading.Timer(THREADING_TIMER, update_latest_weather).start()

    log_string('get latest weather from forecast.io')

    try:

        log_string('Try to get data online...')
        data = requests.get(get_request_url(), timeout=5).json()

        #  get sensor data inside

        sensor_temp_inside = aio_sensors.receive('sensortempinside')
        sensor_temp_inside = float(sensor_temp_inside.value)

        log_string('fetched sensortempinside from adafruit.io: {}'.format(sensor_temp_inside))

        sensor_pressure_inside = aio_sensors.receive('sensorpressureinside')
        sensor_pressure_inside = float(sensor_pressure_inside.value)

        log_string('fetched sensorpressureinside from adafruit.io: {}'.format(sensor_pressure_inside))

        sensor_humidity_inside = aio_sensors.receive('sensorhumidityinside')
        sensor_humidity_inside = float(sensor_humidity_inside.value)

        log_string('fetched sensorhumidityinside from adafruit.io: {}'.format(sensor_humidity_inside))

        #  get sensor data outside

        sensor_temp_outside = aio_sensors.receive('sensortempoutside')
        sensor_temp_outside = float(sensor_temp_outside.value)

        log_string('fetched sensortempoutside from adafruit.io: {}'.format(sensor_temp_outside))

        sensor_pressure_outside = aio_sensors.receive('sensorpressureoutside')
        sensor_pressure_outside = float(sensor_pressure_outside.value)

        log_string('fetched sensorpressureoutside from adafruit.io: {}'.format(sensor_pressure_outside))

        sensor_humidity_outside = aio_sensors.receive('sensorhumidityoutside')
        sensor_humidity_outside = float(sensor_humidity_outside.value)

        log_string('fetched sensorhumidityoutside from adafruit.io: {}'.format(sensor_humidity_outside))

        blink('blue')

        data['currently']['sensor_temp_inside'] = sensor_temp_inside
        data['currently']['sensor_pressure_inside'] = sensor_pressure_inside
        data['currently']['sensor_humidity_inside'] = sensor_humidity_inside

        log_string('added sensor data to temporary json data: '
                   'temp. inside:{} - humidity inside: {} - pressure inside: {}'.format(
                        sensor_temp_inside,
                        sensor_humidity_inside,
                        sensor_pressure_inside
                    ))

        data['currently']['sensor_temp_outside'] = sensor_temp_outside
        data['currently']['sensor_pressure_outside'] = sensor_pressure_outside
        data['currently']['sensor_humidity_outside'] = sensor_humidity_outside

        log_string('added sensor data to temporary json data: '
                   'temp. outside:{} - humidity outside: {} - pressure outside: {}'.format(
                        sensor_temp_outside,
                        sensor_humidity_outside,
                        sensor_pressure_outside
                    ))

        with open('/home/pi/WeatherPi/logs/latest_weather.json', 'w') as outputfile:
            json.dump(data, outputfile, indent=2, sort_keys=True)

        with open('/home/pi/WeatherPi/logs/current_weather.json', 'w') as outputfile:
            json.dump(data['currently'], outputfile, indent=2, sort_keys=True)

        log_string('json data saved to temporary file')

        os.system('cp /home/pi/WeatherPi/logs/latest_weather.json /var/www/html')
        os.system('cp /home/pi/WeatherPi/logs/current_weather.json /var/www/html')

        log_string('json data copied to /var/www/html')

        blink('white')

    except StandardError:

        log_string('ConnectionError - fallback to cached Data')


if __name__ == '__main__':

    update_latest_weather()
