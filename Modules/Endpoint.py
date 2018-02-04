#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os

from Data import Data
from UpdateLog import log_string


class Endpoint(Data):

    def unicorn_pi_data(self):

        rain_forecast = []

        for item in self.hourly_data[:8]:
            rain_percentage = item['precipProbability'] * 100
            rain_forecast.append(round(rain_percentage))

        unicorn_pi_data = {

            "temp": self.temp_api,
            "icon": self.weather_icon,
            "summary": self.forecast,
            "rain_forecast": rain_forecast
        }

        with open('/home/pi/WeatherPi/logs/unicorn_pi_data.json', 'w') as outputfile:
            json.dump(unicorn_pi_data, outputfile, indent=2, sort_keys=True)

        os.system('cp /home/pi/WeatherPi/logs/unicorn_pi_data.json /var/www/html')

        log_string('unicorn_pi_data copied to /var/www/html')


if __name__ == '__main__':
    Endpoint().unicorn_pi_data()
