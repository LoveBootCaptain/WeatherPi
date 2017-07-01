#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

from get_latest_json import *
from init_blinkt import *
from init_io import *


def update_io_thing_speak():

    json_data = get_latest_json()

    api_temperature = json_data['currently']['temperature']
    sensor_temp_outside = json_data['currently']['sensor_temp_outside']
    sensor_temp_inside = json_data['currently']['sensor_temp_inside']

    rain_percentage_data = json_data['currently']['precipProbability']
    rain_percentage = rain_percentage_data * 100

    sensor_pressure_outside = json_data['currently']['sensor_pressure_outside']
    sensor_humidity_outside = json_data['currently']['sensor_humidity_outside']

    payload = {
        'api_key': THINGSPEAK_API_KEY,
        'field1': round(api_temperature, 2),
        'field2': round(sensor_temp_outside, 2),
        'field3': round(sensor_temp_inside, 2),
        'field4': round(rain_percentage, 2),
        'field5': round(sensor_pressure_outside, 2),
        'field6': round(sensor_humidity_outside, 2)
    }

    try:

        log_string('Try sending data to ThingSpeak IO')

        connection = requests.get(THINGSPEAK_URL, params=payload, timeout=2)

        data_id = connection.text

        log_string('Send data to ThingSpeak IO: {}'.format(connection.url))

        log_string('Status Code: {}'.format(connection.status_code))

        log_string('Data ID: {}'.format(data_id))

        blink('blue')

    except StandardError as e:

        log_string('ThingSpeak IO - {} Error'.format(e))


def update_io_adafruit():

    json_data = get_latest_json()

    temp_api = json_data['currently']['temperature']
    sensor_temp_outside = json_data['currently']['sensor_temp_outside']
    sensor_temp_inside = json_data['currently']['sensor_temp_inside']

    rain_percentage_data = json_data['currently']['precipProbability']
    rain_percentage = rain_percentage_data * 100

    forecast = json_data['currently']['summary'].encode('UTF-8')

    daily = json_data['daily']['data']
    forecast_today = daily[0]

    temp_range_today_min = int(forecast_today['temperatureMin'])
    temp_range_today_max = int(forecast_today['temperatureMax'])

    hourly_forecast = json_data['hourly']['summary']

    forecast_today = '{} bis {}°C - {}'.format(
        temp_range_today_min,
        temp_range_today_max,
        hourly_forecast.encode('UTF-8')
    )

    sensor_pressure_outside = json_data['currently']['sensor_pressure_outside']
    sensor_humidity_outside = json_data['currently']['sensor_humidity_outside']

    weather_icon = json_data['currently']['icon']

    feed_list = {
        'temp_api': temp_api,
        'sensor_temp_outside': round(sensor_temp_outside, 2),
        'sensor_temp_inside': round(sensor_temp_inside, 2),
        'rain_percentage': round(rain_percentage, 2),
        'forecast': forecast,
        'forecast_today': forecast_today,
        'sensor_pressure': round(sensor_pressure_outside, 2),
        'sensor_humidity': round(sensor_humidity_outside, 2),
        'weather_icon': weather_icon
    }

    log_string('package for adafruit io: {}'.format(feed_list))
    log_string('Try sending data to Adafruit IO')

    for feed, value in feed_list.items():

        try:

            aio_dashboard.send(feed, value)

            log_string('{}={} successfully send to adafruit.io'.format(feed, value))

        except StandardError as e:

            log_string('Adafruit IO - {} Error - Feed: {} - Value: {}'.format(e, feed, value))

    blink('blue')


if __name__ == '__main__':

    update_io_thing_speak()
    # update_io_adafruit()
