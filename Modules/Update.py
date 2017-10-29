#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import os

from Config import Config
from init_logging import log_string
from init_blinkt import blink
from Adafruit_IO import Client


class Update:
    def __init__(self):

        log_string('Run Update module by: {}'.format(self.__class__))

        ###

        self.config = Config().get_config()

        # set the configs
        self.FORECAST_IO_KEY = self.config['FORECAST_IO_KEY']

        # parameter for the request url
        self.FORECAST_URL = 'https://api.forecast.io/forecast/'  # endpoint for the API

        self.LATITUDE = self.config['LATITUDE']
        self.LONGITUDE = self.config['LONGITUDE']

        self.options = '?lang=de&units=si&exclude=flags'  # some options, see details in API documentation

        self.folder_path = '/home/pi/WeatherPi/Modules/Animations/'

        self.version_path = self.config['UNICORN_VERSION'] + '/'

        self.path = self.folder_path + self.version_path

        self.icon_extension = '.' + 'png'

        self.ADAFRUIT_IO_KEY_SENSORS = self.config['ADAFRUIT_IO_KEY_SENSORS']

        self.aio_sensors = Client(self.ADAFRUIT_IO_KEY_SENSORS)

        try:
            self.data = open('/home/pi/WeatherPi/logs/test_weather_with_alarm.json').read()
            # self.data = open('/home/pi/WeatherPi/logs/latest_weather.json').read()

            self.json_data = json.loads(self.data)

            self.temp_api = self.json_data['currently']['temperature']
            self.sensor_temp_outside = self.json_data['currently']['sensor_temp_outside']
            self.sensor_temp_inside = self.json_data['currently']['sensor_temp_inside']

            self.sensor_pressure_outside = self.json_data['currently']['sensor_pressure_outside']
            self.sensor_humidity_outside = self.json_data['currently']['sensor_humidity_outside']

            self.sensor_pressure_inside = self.json_data['currently']['sensor_pressure_inside']
            self.sensor_humidity_inside = self.json_data['currently']['sensor_humidity_inside']

            self.rain_percentage_data = self.json_data['currently']['precipProbability']
            self.rain_percentage = self.rain_percentage_data * 100

            self.forecast = self.json_data['currently']['summary'].encode('UTF-8')

            self.hourly_data = self.json_data['hourly']['data']

            self.daily = self.json_data['daily']['data']
            self.forecast_today = self.daily[0]

            self.temp_range_today_min = int(self.forecast_today['temperatureMin'])
            self.temp_range_today_max = int(self.forecast_today['temperatureMax'])

            self.hourly_forecast = self.json_data['hourly']['summary']

            self.forecast_today = '{} bis {}°C - {}'.format(
                self.temp_range_today_min,
                self.temp_range_today_max,
                self.hourly_forecast.encode('UTF-8')
            )

            self.weather_icon = self.json_data['currently']['icon']

            self.icon_path = self.path + self.weather_icon + self.icon_extension

        except IOError:

            log_string('ERROR - json file read by module'.format(self.__class__))

    def update_json(self):
        log_string('get latest weather from forecast.io')

        request_url = self.FORECAST_URL + self.FORECAST_IO_KEY + '/' + str(self.LATITUDE) + ',' + \
            str(self.LONGITUDE) + self.options  # build it

        log_string('build request url: {}'.format(request_url))

        try:
            log_string('Try to get data online...')
            self.data = requests.get(request_url, timeout=5).json()

            # Do Stuff

            #  get sensor data inside

            sensor_temp_inside = self.aio_sensors.receive('sensortempinside')
            sensor_temp_inside = float(sensor_temp_inside.value)

            log_string('fetched sensortempinside from adafruit.io: {}'.format(sensor_temp_inside))

            sensor_pressure_inside = self.aio_sensors.receive('sensorpressureinside')
            sensor_pressure_inside = float(sensor_pressure_inside.value)

            log_string('fetched sensorpressureinside from adafruit.io: {}'.format(sensor_pressure_inside))

            sensor_humidity_inside = self.aio_sensors.receive('sensorhumidityinside')
            sensor_humidity_inside = float(sensor_humidity_inside.value)

            log_string('fetched sensorhumidityinside from adafruit.io: {}'.format(sensor_humidity_inside))

            #  get sensor data outside

            sensor_temp_outside = self.aio_sensors.receive('sensortempoutside')
            sensor_temp_outside = float(sensor_temp_outside.value)

            log_string('fetched sensortempoutside from adafruit.io: {}'.format(sensor_temp_outside))

            sensor_pressure_outside = self.aio_sensors.receive('sensorpressureoutside')
            sensor_pressure_outside = float(sensor_pressure_outside.value)

            log_string('fetched sensorpressureoutside from adafruit.io: {}'.format(sensor_pressure_outside))

            sensor_humidity_outside = self.aio_sensors.receive('sensorhumidityoutside')
            sensor_humidity_outside = float(sensor_humidity_outside.value)

            log_string('fetched sensorhumidityoutside from adafruit.io: {}'.format(sensor_humidity_outside))

            blink('blue')

            self.data['currently']['sensor_temp_inside'] = sensor_temp_inside
            self.data['currently']['sensor_pressure_inside'] = sensor_pressure_inside
            self.data['currently']['sensor_humidity_inside'] = sensor_humidity_inside

            log_string('added sensor data to temporary json data: '
                       'temp. inside:{} - humidity inside: {} - pressure inside: {}'.format(
                            sensor_temp_inside,
                            sensor_humidity_inside,
                            sensor_pressure_inside
                        ))

            self.data['currently']['sensor_temp_outside'] = sensor_temp_outside
            self.data['currently']['sensor_pressure_outside'] = sensor_pressure_outside
            self.data['currently']['sensor_humidity_outside'] = sensor_humidity_outside

            log_string('added sensor data to temporary json data: '
                       'temp. outside:{} - humidity outside: {} - pressure outside: {}'.format(
                            sensor_temp_outside,
                            sensor_humidity_outside,
                            sensor_pressure_outside
                        ))

            with open('/home/pi/WeatherPi/logs/latest_weather.json', 'w') as outputfile:
                json.dump(self.data, outputfile, indent=2, sort_keys=True)

            with open('/home/pi/WeatherPi/logs/current_weather.json', 'w') as outputfile:
                json.dump(self.data['currently'], outputfile, indent=2, sort_keys=True)

            log_string('json data saved to temporary file')

            os.system('cp /home/pi/WeatherPi/logs/latest_weather.json /var/www/html')
            os.system('cp /home/pi/WeatherPi/logs/current_weather.json /var/www/html')

            log_string('json data copied to /var/www/html')

            blink('white')

        except StandardError:

            log_string('ConnectionError - fallback to cached Data')


if __name__ == '__main__':
    Update().update_json()


