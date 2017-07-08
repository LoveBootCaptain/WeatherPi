#!/usr/bin/python
# -*- coding: utf-8 -*-

from get_config import get_config
from init_logging import *

# read the config file
config = get_config()

UNICORN_VERSION = config['UNICORN_VERSION']
BRIGHTNESS = config['UNICORN_BRIGHTNESS']

if UNICORN_VERSION == "HD":

    import unicornhathd as unicorn

    log_string('Unicorn Version set to HD')

elif UNICORN_VERSION == "SD":

    import unicornhat as unicorn

    log_string('Unicorn Version set to SD')

else:

    log_string('No valid Unicorn Version found in config file - use "SD" or "HD"')


def unicorn_init():
    unicorn.brightness(BRIGHTNESS)
    if UNICORN_VERSION == "HD":
        unicorn.rotation(0)
    elif UNICORN_VERSION == "SD":
        unicorn.rotation(90)
    else:
        log_string('No valid Unicorn Version found in config file - use "SD" or "HD"')
    unicorn.clear()
    unicorn.show()


if __name__ == '__main__':
    unicorn_init()
