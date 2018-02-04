#!/usr/bin/python
# -*- coding: utf-8 -*-
from Data import Data
from Fonts.custom_font import *
from init_logging import log_string


class SensorData(Data):

    celsius = "*"  # °c
    Celsius = "C"  # C
    unit = "o"  #

    def temp_inside(self):

        sensor_temp_inside = self.sensor_temp_inside

        output_temp = str(int(round(sensor_temp_inside))).zfill(2)

        the_output_data = digits[output_temp[0]] + digits[output_temp[1]] + \
            temp_digits[self.unit[0]] + temp_digits[self.Celsius[0]]

        log_string('Temperature Inside: {}°C'.format(output_temp))

        return the_output_data

    def temp_outside(self):

        sensor_temp_outside = self.sensor_temp_outside
        log_string('sensor_temp_outside: {}'.format(sensor_temp_outside))

        sensor_outside_int = int(round(sensor_temp_outside))
        log_string('sensor_temp_outside rounded: {}'.format(sensor_outside_int))

        sensor_outside_data = str(abs(sensor_outside_int)).zfill(2)
        log_string('format absolute sensor_temp_outside to string: {}'.format(sensor_outside_data))

        if sensor_outside_int < 0:

            plus_minus = "-"
            log_string('Vorzeichen: {}'.format(plus_minus))

        else:

            plus_minus = "+"
            log_string('Vorzeichen: {}'.format(plus_minus))

        the_output_data = temp_digits[plus_minus[0]] + \
            temp_digits[sensor_outside_data[0]] + \
            temp_digits[sensor_outside_data[1]] + \
            temp_digits[self.celsius[0]]

        log_string('Temperature Outside: {}{}°C'.format(plus_minus, sensor_outside_data))

        return the_output_data


if __name__ == '__main__':

    SensorData().temp_inside()
    SensorData().temp_outside()

