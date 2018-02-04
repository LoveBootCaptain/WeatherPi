#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import requests

from Config import Config
from init_blinkt import blink
from init_logging import log_string


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

            log_string('tokens generated')

            return access_token

        except requests.exceptions.HTTPError as error:
            log_string(error.response.status_code)
            log_string(error.response.text)

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
            log_string(error.response.status_code)
            log_string(error.response.text)

    def update_json(self):
        self.update_api()
        self.update_sensors()


if __name__ == '__main__':
    Update().update_json()

