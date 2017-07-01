#!/usr/bin/python
# -*- coding: utf-8 -*-
from Adafruit_IO import Client

from get_config import get_config

# read the config file
config = get_config()

ADAFRUIT_IO_KEY_DASHBOARD = config['ADAFRUIT_IO_KEY_DASHBOARD']
ADAFRUIT_IO_KEY_SENSORS = config['ADAFRUIT_IO_KEY_SENSORS']

aio_dashboard = Client(ADAFRUIT_IO_KEY_DASHBOARD)
aio_sensors = Client(ADAFRUIT_IO_KEY_SENSORS)

THINGSPEAK_API_KEY = config['THINGSPEAK_API_KEY']
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

