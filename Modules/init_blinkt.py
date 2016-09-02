#!/usr/bin/python
# -*- coding: utf-8 -*-
import blinkt
import time
from get_config import get_config
from init_logging import *

# read the config file
config = get_config()

BRIGHTNESS = config['BLINKT_BRIGHTNESS']

leds = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0]

start_time = time.time()


def blinkt_init():

    blinkt.set_brightness(BRIGHTNESS)
    blinkt.clear()
    blinkt.show()


def red_led():

    blinkt_init()

    for i in range(9):

        delta = (time.time() - start_time) * 16

        # Triangle wave, a snappy ping-pong effect
        offset = int(abs((delta % 16) - 8))

        for i in range(8):
            blinkt.set_pixel(i, leds[offset + i], 0, 0)
        blinkt.show()

        time.sleep(0.1)
    blinkt.clear()
    blinkt.show()

    log_string = 'Blinkt: Red'

    print(log_string)
    debug_logger.debug(log_string)


def green_led():

    blinkt_init()

    for i in range(9):

        delta = (time.time() - start_time) * 16

        # Triangle wave, a snappy ping-pong effect
        offset = int(abs((delta % 16) - 8))

        for i in range(8):
            blinkt.set_pixel(i, 0, leds[offset + i], 0)
        blinkt.show()

        time.sleep(0.1)
    blinkt.clear()
    blinkt.show()

    log_string = 'Blinkt: Green'

    print(log_string)
    debug_logger.debug(log_string)


def blue_led():

    blinkt_init()

    for i in range(9):

        delta = (time.time() - start_time) * 16

        # Triangle wave, a snappy ping-pong effect
        offset = int(abs((delta % 16) - 8))

        for i in range(8):
            blinkt.set_pixel(i, 0, 0, leds[offset + i])
        blinkt.show()

        time.sleep(0.1)
    blinkt.clear()
    blinkt.show()

    log_string = 'Blinkt: Blue'

    print(log_string)
    debug_logger.debug(log_string)


def yellow_led():

    blinkt_init()

    for i in range(9):

        delta = (time.time() - start_time) * 16

        # Triangle wave, a snappy ping-pong effect
        offset = int(abs((delta % 16) - 8))

        for i in range(8):
            blinkt.set_pixel(i, leds[offset + i], leds[offset + i], 0)
        blinkt.show()

        time.sleep(0.1)
    blinkt.clear()
    blinkt.show()

    log_string = 'Blinkt: Yellow'

    print(log_string)
    debug_logger.debug(log_string)


def white_led():

    blinkt_init()

    for i in range(9):

        delta = (time.time() - start_time) * 16

        # Triangle wave, a snappy ping-pong effect
        offset = int(abs((delta % 16) - 8))

        for i in range(8):
            blinkt.set_pixel(i, leds[offset + i], leds[offset + i], leds[offset + i])
        blinkt.show()

        time.sleep(0.1)
    blinkt.clear()
    blinkt.show()

    log_string = 'Blinkt: White'

    print(log_string)
    debug_logger.debug(log_string)


if __name__ == '__main__':

    blinkt_init()

    red_led()
    green_led()
    blue_led()
    yellow_led()
    white_led()

    blinkt.clear()
    blinkt.show()
