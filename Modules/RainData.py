#!/usr/bin/python
# -*- coding: utf-8 -*-
from Update import Update

from init_logging import log_string
from Fonts.custom_font import *


class RainData(Update):

    forecast_range_hour = 24  # use len(hourly) for full data (48h)

    percent = "%"

    def rain_probability(self):

        rain_probability = self.rain_percentage_data    # json_data['currently']['precipProbability']

        rain_probability *= 100

        log_string('Regenwahrscheinlichkeit: {}%'.format(rain_probability))

        rain_probability_data = str(int(round(rain_probability))).zfill(2)

        log_string('Regenwahrscheinlichkeit als String für Output: {}%'.format(rain_probability_data))

        the_output_data = digits[rain_probability_data[0]] + digits[rain_probability_data[1]] + temp_digits[self.percent[0]]

        return the_output_data

    def rain_forecast(self):
        percentage_list = []
        color_list = []

        hourly_data = self.hourly_data

        for item in hourly_data:
            rain_percentage = item['precipProbability'] * 100
            percentage_list.append(round(rain_percentage))

        color = 0

        for percentage in percentage_list[:self.forecast_range_hour]:

            if percentage == 0:
                color = "G"  # GREEN
            elif 0 < percentage <= 30:
                color = "Y"  # YELLOW
            elif 31 <= percentage <= 100:
                color = "R"  # RED

            color_list.append(color)

        green_list = [i for i, color in enumerate(color_list) if color == "G"]
        yellow_list = [i for i, color in enumerate(color_list) if color == "Y"]
        red_list = [i for i, color in enumerate(color_list) if color == "R"]

        the_output_data = {
            "GREEN": green_list,
            "YELLOW": yellow_list,
            "RED": red_list
        }

        log_string('Regenwahrscheinlichkeit 24h: {}\n'
                   'Farben auf Display: {}\n'
                   'Farbenliste als Array: {}'.format(
                    percentage_list[:self.forecast_range_hour],
                    color_list,
                    the_output_data
                    ))

        return the_output_data


if __name__ == '__main__':
    RainData().rain_forecast()
    RainData().rain_probability()

