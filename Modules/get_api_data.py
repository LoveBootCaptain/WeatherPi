#!/usr/bin/python
# -*- coding: utf-8 -*-
from get_latest_json import *
from Fonts.custom_font import *
from init_logging import *

celsius = "*"  # °c


def get_temp_api():

    json_data = get_latest_json()

    temp_api = str(int(round(json_data['currently']['temperature'])))

    if temp_api < 0:

        plus_minus = "-"

    else:

        plus_minus = "+"

    the_output_data = temp_digits[plus_minus[0]] + \
                      temp_digits[temp_api[0]] + temp_digits[temp_api[1]] + \
                      temp_digits[celsius[0]]

    log_string('Temperature API: {} {}°C'.format(plus_minus, temp_api))

    return the_output_data
