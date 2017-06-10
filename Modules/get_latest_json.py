#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from init_logging import *


def get_latest_json():

    try:

        data = open('/home/pi/WeatherPi/logs/latest_weather.json').read()

        json_data = json.loads(data)

        log_string('json file read by module')

        return json_data

    except IOError:

        log_string('ERROR - json file read by module')
