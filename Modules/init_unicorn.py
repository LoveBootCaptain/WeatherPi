#!/usr/bin/python
# -*- coding: utf-8 -*-
import unicornhat as unicorn
from get_config import get_config

# read the config file
config = get_config()

BRIGHTNESS = config['UNICORN_BRIGHTNESS']


def unicorn_init():

    unicorn.brightness(BRIGHTNESS)
    unicorn.rotation(90)
    unicorn.clear()
    unicorn.show()


if __name__ == '__main__':

    unicorn_init()
