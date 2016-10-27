#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import threading
from get_latest_json import *
from PIL import Image
from init_unicorn import *
from init_blinkt import red_led
from init_logging import *
from get_config import get_config
import os.path

# read the config file
config = get_config()

THREADING_TIMER = config['THREADING_TIMER']

img = '/home/pi/WeatherPi/Modules/Animations/error.png'


def get_icon():

    # known conditions: clear-day, clear-night, partly-cloudy-day, partly-cloudy-night, windy, cloudy, rain, snow, fog

    json_data = get_latest_json()

    icon = json_data['currently']['icon']

    log_string('Icon to show on Unicorn_HAT: {}'.format(icon))

    return icon


def get_icon_path():

    threading.Timer(10, get_icon_path).start()

    global img

    icon = get_icon()

    base_path = '/home/pi/WeatherPi/Modules/Animations/'

    icon_extension = 'png'

    icon_path = base_path + icon + '.' + icon_extension

    log_string('The Icon Path should be: {}. Checking it...'.format(icon_path))

    # check if file and path are valid

    if os.path.isfile(icon_path):

        log_string('The File: {} is valid and present'.format(icon_path))

        red_led()

        log_string('Updating Unicorn Icon')

        # set new icon_path

        img = icon_path

    else:

        log_string('Error - there is no icon for this weather condition. Please check.')

        red_led()

        log_string('Updating Unicorn Icon')

        # set new icon_path

        icon_path = '/home/pi/WeatherPi/Modules/Animations/error.png'

        img = icon_path


def update_unicorn():

    global img

    unicorn.clear()

    log_string('Start Unicorn Image Loop')

    while img:

        my_img = Image.open(img)

        for o_x in range(int(my_img.size[0] / 8)):

            for o_y in range(int(my_img.size[1] / 8)):

                for x in range(8):

                    for y in range(8):
                        pixel = my_img.getpixel(((o_x * 8) + y, (o_y * 8) + x))
                        # print(pixel)
                        r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                        unicorn.set_pixel(x, y, r, g, b)

                unicorn.show()
                time.sleep(0.25)


if __name__ == '__main__':

    try:
        unicorn_init()
        get_icon_path()
        update_unicorn()

    except KeyboardInterrupt:
        unicorn.clear()
        unicorn.show()
        exit()
