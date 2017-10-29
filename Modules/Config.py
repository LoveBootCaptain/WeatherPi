#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from init_logging import log_string


class Config:
    def __init__(self):

        # read the config file
        self.config_data = open('/home/pi/WeatherPi/config.json').read()

        self.config = json.loads(self.config_data)

        log_string('config file read by module {}'.format(self.__class__))

    def get_config(self):
        return self.config


if __name__ == '__main__':
    Config().get_config()
