#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
# import threading
from get_latest_json import *
from init_blinkt import blue_led
from init_io import *

THREADING_TIMER = config['THREADING_TIMER']


def update_io_thing_speak():

    # threading.Timer(THREADING_TIMER, update_io_thing_speak).start()

    json_data = get_latest_json()

    api_temperature = json_data['currently']['temperature']
    sensor_temp_outside = json_data['currently']['sensor_temp_outside']
    sensor_temp_inside = json_data['currently']['sensor_temp_inside']

    rain_percentage_data = json_data['currently']['precipProbability']
    rain_percentage = rain_percentage_data * 100

    sensor_pressure_outside = json_data['currently']['sensor_pressure_outside']
    sensor_humidity_outside = json_data['currently']['sensor_humidity_outside']

    io_url = BASE_URL + '&field1={}&field2={}&field3={}&field4={}&field5={}&field6={}'.format(
        round(api_temperature, 2),
        round(sensor_temp_outside, 2),
        round(sensor_temp_inside, 2),
        round(rain_percentage, 2),
        round(sensor_pressure_outside, 2),
        round(sensor_humidity_outside, 2)
    )

    try:
        connection = urllib.urlopen(io_url)

        connection.read()

        log_string('Send data to ThingSpeak IO: {}'.format(io_url))

        connection.close()

        blue_led()

    except IOError:

        log_string('ThingSpeak IO - Connection Error')


def update_io_adafruit():

    # threading.Timer(THREADING_TIMER, update_io_adafruit).start()

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

    for feed, value in feed_list.items():

        try:
            aio_dashboard.send(feed, value)

            log_string('{}={} send to adafruit.io'.format(feed, value))

        except IOError:

            log_string('Adafruit IO - Connection Error - Feed: {} - Value: {}'.format(feed, value))

    blue_led()


if __name__ == '__main__':

    update_io_thing_speak()
    update_io_adafruit()
