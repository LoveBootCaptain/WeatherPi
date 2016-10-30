#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
# import threading
from get_latest_json import *
from PIL import Image
from init_unicorn import *
from init_blinkt import *
from init_logging import *
from get_config import get_config
import os.path

# read the config file
config = get_config()

THREADING_TIMER = config['THREADING_TIMER']

img_file = '/home/pi/WeatherPi/Modules/Animations/error.png'

folder_path = '/home/pi/WeatherPi/Modules/Animations/'

icon_extension = '.' + 'png'


def get_icon():

    # known conditions: clear-day, clear-night, partly-cloudy-day, partly-cloudy-night, windy, cloudy, rain, snow, fog

    json_data = get_latest_json()

    icon = json_data['currently']['icon']

    log_string('Icon to show on Unicorn_HAT: {}'.format(icon))

    return icon


def get_icon_path():

    # threading.Timer(10, get_icon_path).start()

    global img_file

    icon = get_icon()

    icon_path = folder_path + icon + icon_extension

    log_string('The icon path should be: {}. Checking it...'.format(icon_path))

    # check if file and path are valid

    if os.path.isfile(icon_path):

        log_string('The File: {} is valid and present!'.format(icon_path))

        log_string('Updating Unicorn with new weather condition icon: {}.'.format(icon))

        # set new icon_path

        img_file = icon_path

        blink('red')

    else:

        log_string('Error - there is no icon for this weather condition. Please check.')

        log_string('Updating Unicorn icon to error screen')

        # set new icon_path

        icon_path = '/home/pi/WeatherPi/Modules/Animations/error.png'

        img_file = icon_path

        blink('red')


def update_unicorn():

    global img_file

    unicorn.clear()

    log_string('Start Unicorn image loop')

    while img_file:

        img = Image.open(img_file)

        draw_unicorn(img)


def draw_unicorn(image):

    for o_x in range(int(image.size[0] / 8)):

        for o_y in range(int(image.size[1] / 8)):

            for x in range(8):

                for y in range(8):
                    pixel = image.getpixel(((o_x * 8) + y, (o_y * 8) + x))
                    # print(pixel)
                    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                    unicorn.set_pixel(x, y, r, g, b)

            unicorn.show()
            time.sleep(0.25)


def test_unicorn():

    print('Testing all images in folder {}'.format(folder_path))

    for file in os.listdir(folder_path):

        if file.endswith(icon_extension):

            print('Testing image: {}'.format(folder_path + file))

            img = Image.open(folder_path + file)

            draw_unicorn(img)

        else:

            print('Not using this file, not an image: {}'.format(file))


if __name__ == '__main__':

    try:

        unicorn_init()

        test_unicorn()

        get_icon_path()
        update_unicorn()

    except KeyboardInterrupt:
        unicorn.clear()
        unicorn.show()
        exit()
