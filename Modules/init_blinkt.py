#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import blinkt

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


def blink(color):

    blinkt_init()

    for y in range(9):

        delta = (time.time() - start_time) * 16

        # Triangle wave, a snappy ping-pong effect
        offset = int(abs((delta % 16) - 8))

        if color == 'white':

            for i in range(8):

                blinkt.set_pixel(i, leds[offset + i], leds[offset + i], leds[offset + i])

            blinkt.show()

        elif color == 'red':

            for i in range(8):

                blinkt.set_pixel(i, leds[offset + i], 0, 0)

            blinkt.show()

        elif color == 'yellow':

            for i in range(8):

                blinkt.set_pixel(i, leds[offset + i], leds[offset + i], 0)

            blinkt.show()

        elif color == 'blue':

            for i in range(8):

                blinkt.set_pixel(i, 0, 0, leds[offset + i])

            blinkt.show()

        elif color == 'green':

            for i in range(8):

                blinkt.set_pixel(i, 0, leds[offset + i], 0)

            blinkt.show()

        else:

            log_string('ERROR: Blinkt Color {} not set. Showing white.'.format(color))

            for i in range(8):

                blinkt.set_pixel(i, leds[offset + i], leds[offset + i], leds[offset + i])

            blinkt.show()

        time.sleep(0.1)

    blinkt.clear()
    blinkt.show()

    log_string('Blinkt: {}'.format(color))


if __name__ == '__main__':

    blinkt_init()

    blink('white')
    blink('red')
    blink('blue')
    blink('yellow')
    blink('green')

    blinkt.clear()
    blinkt.show()
