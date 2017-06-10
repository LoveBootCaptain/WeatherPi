#!/usr/bin/python
# -*- coding: utf-8 -*-
from Driver.BicolorBargraph24 import BicolorBargraph24
from Driver.Matrix16x8 import Matrix16x8
from get_config import get_config

# read the config file
config = get_config()

BRIGHTNESS = config['MATRIX_BRIGHTNESS']

matrix_green = Matrix16x8(address=0x70)
matrix_red = Matrix16x8(address=0x71)
matrix_blue = Matrix16x8(address=0x72)
matrix_orange = Matrix16x8(address=0x73)

bargraph = BicolorBargraph24(address=0x74)

matrix_list = (matrix_green, matrix_red, matrix_blue, matrix_orange)


def matrix_init():
    global matrix_list
    for matrix in matrix_list:
        matrix.begin()
        matrix.clear()
        matrix.set_brightness(BRIGHTNESS)
        matrix.write_display()

    bargraph.begin()
    bargraph.clear()
    bargraph.set_brightness(BRIGHTNESS)
    bargraph.write_display()


if __name__ == '__main__':

    matrix_init()
