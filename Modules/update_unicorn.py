#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
# import threading
from Modules.get_latest_json import *
from PIL import Image
from Modules.init_unicorn import *
from Modules.init_blinkt import red_led
from Modules.init_logging import *
from Modules.get_config import get_config

# read the config file
config = get_config()

THREADING_TIMER = config['THREADING_TIMER']


def get_icon():

    json_data = get_latest_json()

    icon = json_data['currently']['icon']

    log_string = 'Icon to show on Unicorn_HAT: {}'.format(icon)

    print(log_string)
    debug_logger.debug(log_string)

    if icon == 'clear-day':

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/sunny.png')

    elif icon == 'clear-night':

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/moon.png')

    elif icon == 'partly-cloudy-day':

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/cloudy_day.png')

    elif icon == 'partly-cloudy-night':

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/cloudy_night.png')

    elif icon == 'windy':

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/windy.png')

    elif icon == 'cloudy':

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/cloudy.png')

    elif icon == 'rain':

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/rain.png')

    elif icon == 'snow':

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/snow.png')

    else:

        img = Image.open('/home/pi/WeatherPi/Modules/Animations/error.png')

    return img


def update_unicorn():

    # threading.Timer(THREADING_TIMER, update_unicorn).start()

    # my_current_img = current_img

    img = get_icon()

    red_led()

    unicorn.clear()

    # while True:

    for i in range(23):

        for o_x in range(int(img.size[0] / 8)):

            for o_y in range(int(img.size[1] / 8)):

                for x in range(8):

                    for y in range(8):
                        pixel = img.getpixel(((o_x * 8) + y, (o_y * 8) + x))
                        # print(pixel)
                        r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
                        unicorn.set_pixel(x, y, r, g, b)

                unicorn.show()
                time.sleep(0.25)


if __name__ == '__main__':

    try:
        unicorn_init()
        update_unicorn()
    except KeyboardInterrupt:
        unicorn.clear()
        unicorn.show()
        exit()
