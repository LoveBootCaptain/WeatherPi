#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path

from PIL import Image

from get_latest_json import *
from init_blinkt import *
from init_unicorn import *

# read the config file
config = get_config()

folder_path = '/home/pi/WeatherPi/Modules/Animations/'

version_path = config['UNICORN_VERSION'] + '/'

icon_extension = '.' + 'png'

img_file = folder_path + version_path + 'error' + icon_extension

width, height = unicorn.get_shape()


def get_icon():
    # known conditions: clear-day, clear-night, partly-cloudy-day, partly-cloudy-night, wind, cloudy, rain, snow, fog

    json_data = get_latest_json()

    icon = json_data['currently']['icon']

    log_string('Icon to show on Unicorn_HAT: {}'.format(icon))

    return icon


def get_icon_path():
    global img_file

    icon = get_icon()

    icon_path = folder_path + version_path + icon + icon_extension

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

        icon_path = folder_path + version_path + 'error' + icon_extension

        img_file = icon_path

        blink('red')


def update_unicorn():
    unicorn.clear()

    global img_file

    log_string('Start Unicorn image loop')

    while img_file:

        img = Image.open(img_file)

        draw_unicorn(img)

    else:

        log_string('Something went wrong while picking up the img')
        return


def draw_unicorn(image):
    # this is the original pimoroni function for drawing sprites

    for o_x in range(int(image.size[0] / width)):

        for o_y in range(int(image.size[1] / height)):

            valid = False

            for x in range(width):

                for y in range(height):
                    pixel = image.getpixel(((o_x * width) + y, (o_y * height) + x))
                    # print(pixel)
                    r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                    if r or g or b:
                        valid = True
                    unicorn.set_pixel(x, y, r, g, b)

            if valid:
                unicorn.show()
                time.sleep(0.25)


def test_unicorn():
    print('Testing all images in folder {}'.format(folder_path + version_path))

    for image in os.listdir(folder_path + version_path):

        if image.endswith(icon_extension):

            print('Testing image: {}'.format(folder_path + version_path + image))

            img = Image.open(folder_path + version_path + image)

            draw_unicorn(img)

        else:

            print('Not using this file, not an image: {}'.format(file))

    unicorn.clear()
    unicorn.show()


def draw_single_icon(animation):
    unicorn.clear()

    single_file = folder_path + version_path + animation + icon_extension

    log_string('Start drawing single icon or animation: {}'.format(animation))

    img = Image.open(single_file)

    draw_unicorn(img)


if __name__ == '__main__':

    try:

        unicorn_init()
        draw_single_icon('raspberry_boot')
        test_unicorn()
        get_icon_path()
        update_unicorn()

    except KeyboardInterrupt:

        unicorn.clear()
        unicorn.show()
