#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from Data import Data
from init_blinkt import *
from init_logging import weather_logger


class UpdateLog(Data):
    def create_log(self):

        current_time = datetime.now().isoformat()

        io_str = '{} bis {}°C - {}'.format(
            self.temp_range_today_min,
            self.temp_range_today_max,
            self.hourly_forecast.encode('UTF-8')
        )

        latitude = config['LATITUDE']
        longitude = config['LONGITUDE']

        log_string_base = '[timestamp={}], [temp_api={}], [sensor_temp_inside={}], [sensor_temp_outside={}], ' \
                          '[rain_percentage={}], [sensor_pressure_inside={}], [sensor_humidity_inside={}],' \
                          '[sensor_humidity_outside={}], [summary="{}"],' \
                          ' [next_weather_today="{}"], [latitude={}], [longitude={}]]'.format(
                            current_time,
                            self.temp_api,
                            self.sensor_temp_wohnzimmer,
                            self.sensor_temp_outside,
                            self.rain_percentage,
                            self.sensor_pressure_wohnzimmer,
                            self.sensor_humidity_wohnzimmer,
                            self.sensor_humidity_outside,
                            self.forecast,
                            io_str,
                            latitude,
                            longitude
        )

        # write log_string to log file
        weather_logger.info(log_string_base)

        log_string('created log entry: {}'.format(log_string_base))

        blink('green')


if __name__ == '__main__':

    UpdateLog().create_log()

