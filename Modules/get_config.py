#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from init_logging import *

# read the config file
config_data = open('/home/pi/WeatherPi/config.json').read()


def get_config():

    config = json.loads(config_data)

    log_string('config file read by module')

    return config
