#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path

from PIL import Image

from Data import Data
from init_blinkt import *
from init_unicorn import *

img_file = None

width, height = unicorn.get_shape()


class UpdateIcon(Data):

    def set_icon_path(self):

        global img_file

        """
        known conditions: clear-day, clear-night, partly-cloudy-day, partly-cloudy-night, wind, cloudy, rain, snow, fog
        """

        icon = self.weather_icon

        log_string('Icon to show on Unicorn_HAT: {}'.format(icon))

        icon_path = self.icon_path

        log_string('The icon path should be: {}. Checking it...'.format(icon_path))
        # check if file and path are valid
        if os.path.isfile(icon_path):

            log_string('The File: {} is valid and present!'.format(icon_path))
            log_string('Updating Unicorn with new weather condition icon: {}.'.format(icon))

            # set new icon_path
            img_file = icon_path

            blink('red')

            return img_file

        else:

            log_string('Error - there is no icon for this weather condition. Please check.')

            log_string('Updating Unicorn icon to error screen')

            # set new icon_path

            icon_path = self.path + 'error' + self.icon_extension

            img_file = icon_path

            blink('red')

            return img_file


class UniCorn(Data):

    def update_unicorn(self):

        unicorn.clear()

        global img_file

        log_string('Start Unicorn image loop')

        while img_file:

            img = Image.open(img_file)

            self.draw_unicorn(img)

        else:

            log_string('Something went wrong while picking up the img')
            pass

    @staticmethod
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

    def test_unicorn(self):
        print('Testing all images in folder {}'.format(self.path))

        for image in os.listdir(self.path):

            if image.endswith(self.icon_extension):

                print('Testing image: {}'.format(self.path + image))

                img = Image.open(self.path + image)

                self.draw_unicorn(img)

            else:

                print('Not using this file, not an image: {}'.format(file))

        unicorn.clear()
        unicorn.show()

    def draw_single_icon(self, animation):
        unicorn.clear()

        single_file = self.path + animation + self.icon_extension

        log_string('Start drawing single icon or animation: {}'.format(animation))

        img = Image.open(single_file)

        self.draw_unicorn(img)


if __name__ == '__main__':

    try:

        unicorn_init()
        UniCorn().draw_single_icon('raspberry_boot')
        # UniCorn().test_unicorn()
        UpdateIcon().set_icon_path()
        UniCorn().update_unicorn()

    except KeyboardInterrupt:

        unicorn.clear()
        unicorn.show()
