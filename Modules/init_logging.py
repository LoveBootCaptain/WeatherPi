#!/usr/bin/python
# -*- coding: utf-8 -*-
# create some logger details
import logging.handlers
import socket

host = socket.gethostname()

# create a weather logger

weather_path = '/home/pi/WeatherPi/logs/Weather_Log_Data_{}.log'.format(host)
WEATHER_LOG_FILENAME = weather_path

# Set up a specific logger with our desired output level
weather_logger = logging.getLogger('WeatherLogger')
weather_logger.setLevel(logging.INFO)

# Add the log message handler to the logger and make a log-rotation of 100 files with max. 10MB per file
weather_handler = logging.handlers.RotatingFileHandler(WEATHER_LOG_FILENAME, maxBytes=10485760, backupCount=100)
weather_logger.addHandler(weather_handler)


# create a debug logger

debug_path = '/home/pi/WeatherPi/logs/Debug_Log_{}.log'.format(host)
DEBUG_LOG_FILENAME = debug_path

# Set up a specific logger with our desired output level
debug_logger = logging.getLogger('DebugLogger')
debug_logger.setLevel(logging.DEBUG)


# Add the log message handler to the logger and make a log-rotation of 100 files with max. 10MB per file
debug_handler = logging.handlers.RotatingFileHandler(DEBUG_LOG_FILENAME, maxBytes=100000, backupCount=1)
debug_logger.addHandler(debug_handler)


def log_string(string):

    print(string)
    debug_logger.debug(string)
