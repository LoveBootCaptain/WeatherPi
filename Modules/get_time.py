#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import time

from Fonts import custom_font

hours_colon = custom_font.hours
hours_no_colon = custom_font.hours_no_colon
digits = custom_font.digits

colon_on = True


def get_time():

    threading.Timer(1, get_time).start()

    global colon_on

    the_hour = time.strftime("%I")
    the_min = time.strftime("%M")

    if the_hour.startswith("0"):
        the_hour = the_hour[1:]

    if colon_on:
        colon_on = False
        the_hour_data = hours_colon[the_hour]
    else:
        colon_on = True
        the_hour_data = hours_no_colon[the_hour]

    the_min_data = digits[the_min[0]] + digits[the_min[1]]
    time_buffer = the_hour_data + the_min_data

    # log_string = 'Time: {}:{}'.format(the_hour, the_min)
    #
    # print(log_string)
    # debug_logger.debug(log_string)

    return time_buffer
