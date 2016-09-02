#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

# read the config file
config_data = open('/home/pi/WeatherPi/config.json').read()


def get_config():

    config = json.loads(config_data)

    return config
