#!/usr/bin/python
# -*- coding: utf-8 -*-
from Modules.Fonts.custom_font import *
from Modules.get_latest_json import *
from Modules.init_logging import *

celsius = "*"  # °c
Celsius = "C"  # C
unit = "o"  #


def get_sensor_temp_inside():

    sensor_temp_inside = get_latest_json()['currently']['sensor_temp_inside']

    output_temp = str(int(round(sensor_temp_inside))).zfill(2)

    the_output_data = digits[output_temp[0]] + digits[output_temp[1]] + \
                      temp_digits[unit[0]] + temp_digits[Celsius[0]]

    log_string = 'Temperature Inside: {}°C'.format(output_temp)

    print(log_string)
    debug_logger.debug(log_string)

    return the_output_data


def get_sensor_temp_outside():

    sensor_temp_outside = get_latest_json()['currently']['sensor_temp_outside']
    sensor_outside_int = int(round(sensor_temp_outside))
    sensor_outside_data = str(sensor_outside_int).zfill(2)

    if sensor_outside_int < 0:
        plus_minus = "-"
    else:
        plus_minus = "+"

    the_output_data = temp_digits[plus_minus[0]] + \
                      temp_digits[sensor_outside_data[0]] + temp_digits[sensor_outside_data[1]] + \
                      temp_digits[celsius[0]]

    log_string = 'Temperature Outside: {} {}°C'.format(plus_minus, sensor_outside_data)

    print(log_string)
    debug_logger.debug(log_string)

    return the_output_data

if __name__ == '__main__':
    get_sensor_temp_inside()
    get_sensor_temp_outside()

