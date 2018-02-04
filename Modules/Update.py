#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import os

from Config import Config
from init_logging import log_string
from init_blinkt import blink


class Update:
    def __init__(self):

        log_string('Run Update module by: {}'.format(self.__class__))

        # set the configs
        self.config = Config().get_config()

        # parameter for the api request.rqst url
        self.FORECAST_IO_KEY = self.config['FORECAST_IO_KEY']
        self.LATITUDE = self.config['LATITUDE']
        self.LONGITUDE = self.config['LONGITUDE']
        self.FORECAST_URL = 'https://api.forecast.io/forecast/'  # endpoint for the API
        self.options = '?lang=de&units=si&exclude=flags'  # some options, see details in API documentation

        # parameter for the sensor request.rqst url
        self.username = self.config['NETATMO_USERNAME']
        self.password = self.config['NETATMO_PASSWORD']
        self.client_id = self.config['NETATMO_CLIENT_ID']
        self.client_secret = self.config['NETATMO_CLIENT_SECRET']
        self.device_id = self.config['NETATMO_DEVICE_ID']

    def update_api(self):
        log_string('get latest weather from forecast.io')

        api_request_url = self.FORECAST_URL + self.FORECAST_IO_KEY + '/' + str(self.LATITUDE) + ',' + \
            str(self.LONGITUDE) + self.options

        log_string('build request url: {}'.format(api_request_url))

        try:
            log_string('Try to get data online...')
            data = requests.get(api_request_url, timeout=5).json()

            # save data dict as json file
            with open('/home/pi/WeatherPi/logs/latest_weather.json', 'w') as outputfile:
                json.dump(data, outputfile, indent=2, sort_keys=True)

            with open('/home/pi/WeatherPi/logs/current_weather.json', 'w') as outputfile:
                json.dump(data['currently'], outputfile, indent=2, sort_keys=True)

            log_string('json data saved to temporary file')

            os.system('cp /home/pi/WeatherPi/logs/latest_weather.json /var/www/html')
            os.system('cp /home/pi/WeatherPi/logs/current_weather.json /var/www/html')

            log_string('api json data copied to /var/www/html')

            blink('white')

        except StandardError:

            log_string('ConnectionError - fallback to cached Data')

    def auth_netatmo(self):

        payload = {'grant_type': 'password',
                   'username': self.username,
                   'password': self.password,
                   'client_id': self.client_id,
                   'client_secret': self.client_secret,
                   'scope': 'read_station'}

        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
            access_token = response.json()["access_token"]
            refresh_token = response.json()["refresh_token"]
            scope = response.json()["scope"]
            print("Your access token is:", access_token)
            print("Your refresh token is:", refresh_token)
            print("Your scopes are:", scope)

            return access_token

        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)

    def update_sensors(self):

        payload = {
            'access_token': self.auth_netatmo(),
            'device_id': self.device_id
        }

        try:
            response = requests.post("https://api.netatmo.com/api/getstationsdata", params=payload)
            response.raise_for_status()
            data = response.json()["body"]

            # save data dict as json file
            with open('/home/pi/WeatherPi/logs/sensors.json', 'w') as outputfile:
                json.dump(data, outputfile, indent=2, sort_keys=True)

            log_string('sensor data saved to /logs')
            return data

        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)

    def update_json(self):
        self.update_api()
        self.update_sensors()


if __name__ == '__main__':
    Update().update_json()


# # variables for weather icon
# self.version_path = self.config['UNICORN_VERSION'] + '/'
# self.folder_path = '/home/pi/WeatherPi/Modules/Animations/'
# self.path = self.folder_path + self.version_path
# self.icon_extension = '.' + 'png'

# # all variables from json file
# try:
#     # self.data = open('/home/pi/WeatherPi/logs/test_weather_with_alarm.json').read()
#     self.data = open('/home/pi/WeatherPi/logs/latest_weather.json').read()
#
#     self.json_data = json.loads(self.data)
#
#     # api data
#     self.temp_api = self.json_data['currently']['temperature']
#     self.rain_percentage_data = self.json_data['currently']['precipProbability']
#     self.rain_percentage = self.rain_percentage_data * 100
#     self.forecast = self.json_data['currently']['summary'].encode('UTF-8')
#     self.weather_icon = self.json_data['currently']['icon']
#     self.hourly_data = self.json_data['hourly']['data']
#     self.hourly_forecast = self.json_data['hourly']['summary']
#     self.daily = self.json_data['daily']['data']
#     self.forecast_today = self.daily[0]
#     self.temp_range_today_min = int(self.forecast_today['temperatureMin'])
#     self.temp_range_today_max = int(self.forecast_today['temperatureMax'])
#
#     # generated string
#     self.forecast_today = '{} bis {}°C - {}'.format(
#         self.temp_range_today_min,
#         self.temp_range_today_max,
#         self.hourly_forecast.encode('UTF-8')
#     )
#
#     self.icon_path = self.path + self.weather_icon + self.icon_extension
#
# except IOError:
#
#     log_string('ERROR - json file read by module'.format(self.__class__))


# # sensor data
# self.sensor_temp_outside = self.json_data['currently']['sensor_temp_outside']
# self.sensor_temp_inside = self.json_data['currently']['sensor_temp_inside']
# self.sensor_pressure_outside = self.json_data['currently']['sensor_pressure_outside']
# self.sensor_humidity_outside = self.json_data['currently']['sensor_humidity_outside']
# self.sensor_pressure_inside = self.json_data['currently']['sensor_pressure_inside']
# self.sensor_humidity_inside = self.json_data['currently']['sensor_humidity_inside']

# #  get sensor data inside
# sensor_temp_inside = 0
# log_string('fetched sensortempinside from adafruit.io: {}'.format(sensor_temp_inside))
#
# sensor_pressure_inside = 0
# log_string('fetched sensorpressureinside from adafruit.io: {}'.format(sensor_pressure_inside))
#
# sensor_humidity_inside = 0
# log_string('fetched sensorhumidityinside from adafruit.io: {}'.format(sensor_humidity_inside))
#
# #  get sensor data outside
# sensor_temp_outside = 0
# log_string('fetched sensortempoutside from adafruit.io: {}'.format(sensor_temp_outside))
#
# sensor_pressure_outside = 0
# log_string('fetched sensorpressureoutside from adafruit.io: {}'.format(sensor_pressure_outside))
#
# sensor_humidity_outside = 0
# log_string('fetched sensorhumidityoutside from adafruit.io: {}'.format(sensor_humidity_outside))
#
# blink('blue')
#
# # add data to data dict
# self.data['currently']['sensor_temp_inside'] = sensor_temp_inside
# self.data['currently']['sensor_pressure_inside'] = sensor_pressure_inside
# self.data['currently']['sensor_humidity_inside'] = sensor_humidity_inside
#
# log_string('added sensor data to temporary json data: '
#            'temp. inside:{} - humidity inside: {} - pressure inside: {}'.format(
#                 sensor_temp_inside,
#                 sensor_humidity_inside,
#                 sensor_pressure_inside
#             ))
#
# self.data['currently']['sensor_temp_outside'] = sensor_temp_outside
# self.data['currently']['sensor_pressure_outside'] = sensor_pressure_outside
# self.data['currently']['sensor_humidity_outside'] = sensor_humidity_outside
#
# log_string('added sensor data to temporary json data: '
#            'temp. outside:{} - humidity outside: {} - pressure outside: {}'.format(
#                 sensor_temp_outside,
#                 sensor_humidity_outside,
#                 sensor_pressure_outside
#             ))
#
#
# forecast = RainData()
#
# small_json = {
#
#     "temp_api": self.temp_api,
#     "temp_in": self.sensor_temp_inside,
#     "temp_out": self.sensor_temp_outside,
#     "icon": self.weather_icon,
#     "summary": self.forecast,
#     "rain_probability": self.rain_percentage,
#     "rain_forecast": forecast.rain_forecast()
#
# }
#
# print(small_json)
#
# with open('/home/pi/WeatherPi/logs/small_weather.json', 'w') as outputfile:
#     json.dump(small_json, outputfile, indent=2, sort_keys=True)
