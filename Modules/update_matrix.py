#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
# import time
from Modules.init_matrix import *
from Modules.get_sensor_data import *
# from get_api_data import *
# from init_blinkt import red_led
from Modules.get_rain_forecast import *
# from init_logging import *
from Modules.get_config import get_config

# read the config file
config = get_config()

THREADING_TIMER = config['THREADING_TIMER']

matrix_init()


def update_matrix():

    # threading.Timer(THREADING_TIMER, update_matrix).start()

    sensor_temp_outside = get_sensor_temp_outside()
    rain_probability = get_rain_probability()
    sensor_temp_inside = get_sensor_temp_inside()

    update_list = {
        1: ('Grüne Matrix', matrix_green, 'sensor_temp_outside', sensor_temp_outside),
        2: ('Orange Matrix', matrix_orange, 'rain_probability', rain_probability),
        3: ('Rote Matrix', matrix_red, 'sensor_temp_inside', sensor_temp_inside)
    }

    try:

        for matrix, value in update_list.items():

            value[1].clear()
            value[1].display_16x8_buffer(value[3])
            value[1].write_display()
            log_string = '{} updated mit {} - {}'.format(value[0], value[2], value[3])
            print(log_string)
            debug_logger.debug(log_string)
            red_led()
            time.sleep(0.25)

    except IOError:

        log_string = 'Matrix Error'

        print(log_string)
        debug_logger.debug(log_string)

        return


def update_bargraph():

    # threading.Timer(THREADING_TIMER, update_bargraph).start()

    try:

        bargraph.clear()

        rain_forecast = get_rain_forecast()

        for i in rain_forecast["GREEN"]:
            bargraph.set_bar(i, GREEN)

        for i in rain_forecast["YELLOW"]:
            bargraph.set_bar(i, YELLOW)

        for i in rain_forecast["RED"]:
            bargraph.set_bar(i, RED)

        log_string = 'Bargraph Updated GREEN: {},\n' \
                     'Bargraph Updated YELLOW: {},\n' \
                     'Bargraph Updated RED: {}'.format(
            rain_forecast["GREEN"],
            rain_forecast["YELLOW"],
            rain_forecast["RED"]
        )

        print(log_string)
        debug_logger.debug(log_string)

        bargraph.write_display()

        red_led()

    except IOError:

        log_string = 'Bargraph Error'

        print(log_string)
        debug_logger.debug(log_string)

        return

hours_colon = hours
hours_no_colon = hours_no_colon
digits = digits

colon_on = True


def update_clock_matrix():

    threading.Timer(1, update_clock_matrix).start()

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

    try:

        matrix_blue.clear()

        matrix_blue.display_16x8_buffer(time_buffer)
        matrix_blue.write_display()

        # log_string = 'Blue Matrix (Time) updated - {}:{} - {}'.format(the_hour, the_min, time_buffer)
        #
        # print(log_string)
        # debug_logger.debug(log_string)

    except IOError:

        log_string = 'Clock Matrix Error'

        print(log_string)
        debug_logger.debug(log_string)

        return

if __name__ == '__main__':

    try:
        update_bargraph()
        update_clock_matrix()
        update_matrix()
    except (KeyboardInterrupt, IOError):
        from clear import *
        clear_all()

