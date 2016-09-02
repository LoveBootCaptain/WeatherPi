#!/usr/bin/python
# -*- coding: utf-8 -*-
from Modules.init_matrix import *
from Modules.init_unicorn import *
from Modules.init_blinkt import *


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


if __name__ == '__main__':

    clear_all()
