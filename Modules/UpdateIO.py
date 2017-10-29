#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

from Update import Update
from init_blinkt import *
from Adafruit_IO import Client


class UpdateIO(Update):

    ADAFRUIT_IO_KEY_DASHBOARD = config['ADAFRUIT_IO_KEY_DASHBOARD']

    aio_dashboard = Client(ADAFRUIT_IO_KEY_DASHBOARD)

    THINGSPEAK_API_KEY = config['THINGSPEAK_API_KEY']
    THINGSPEAK_URL = 'https://api.thingspeak.com/update'

    def send_io_thing_speak(self):

        payload = {
            'api_key': self.THINGSPEAK_API_KEY,
            'field1': round(self.temp_api, 2),
            'field2': round(self.sensor_temp_outside, 2),
            'field3': round(self.sensor_temp_inside, 2),
            'field4': round(self.rain_percentage, 2),
            'field5': round(self.sensor_pressure_outside, 2),
            'field6': round(self.sensor_humidity_outside, 2)
        }

        try:

            log_string('Try sending data to ThingSpeak IO')

            connection = requests.get(self.THINGSPEAK_URL, params=payload, timeout=2)

            data_id = connection.text

            log_string('Send data to ThingSpeak IO: {}'.format(connection.url))

            log_string('Status Code: {}'.format(connection.status_code))

            log_string('Data ID: {}'.format(data_id))

            blink('blue')

        except StandardError as e:

            log_string('ThingSpeak IO - {} Error'.format(e))

    def send_io_adafruit(self):

        feed_list = {
            'temp_api': self.temp_api,
            'sensor_temp_outside': round(self.sensor_temp_outside, 2),
            'sensor_temp_inside': round(self.sensor_temp_inside, 2),
            'rain_percentage': round(self.rain_percentage, 2),
            'forecast': self.forecast,
            'forecast_today': self.forecast_today,
            'sensor_pressure': round(self.sensor_pressure_outside, 2),
            'sensor_humidity': round(self.sensor_humidity_outside, 2),
            'weather_icon': self.weather_icon
        }

        log_string('package for adafruit io: {}'.format(feed_list))
        log_string('Try sending data to Adafruit IO')

        for feed, value in feed_list.items():

            try:

                self.aio_dashboard.send(feed, value)

                log_string('{}={} successfully send to adafruit.io'.format(feed, value))

            except StandardError as e:

                log_string('Adafruit IO - {} Error - Feed: {} - Value: {}'.format(e, feed, value))

    def send_iot_data(self):
        self.send_io_thing_speak()
        self.send_io_adafruit()
        blink('blue')


if __name__ == '__main__':

    UpdateIO().send_iot_data()
