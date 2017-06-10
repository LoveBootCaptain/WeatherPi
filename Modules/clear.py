#!/usr/bin/python
# -*- coding: utf-8 -*-
from init_matrix import *
from init_unicorn import *
from init_blinkt import *
from init_logging import *


def clear_all():

    for matrix in matrix_list:

        matrix.clear()
        matrix.write_display()

    bargraph.clear()
    bargraph.write_display()

    unicorn.clear()
    unicorn.show()

    blinkt.clear()
    blinkt.show()

    log_string('Clear Display')


if __name__ == '__main__':

    clear_all()
