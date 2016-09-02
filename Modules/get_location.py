#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from init_logging import *


# get location for weather requests
def get_location():
    try:
        location_request_url = 'http://ip-api.com/json'
        location_data = requests.get(location_request_url).json()
        log_string = 'location data received'

        print(log_string)
        debug_logger.debug(log_string)

        return location_data

    except IOError:

        log_string = 'ERROR - location data received'

        print(log_string)
        debug_logger.debug(log_string)

if __name__ == '__main__':
    get_location()
