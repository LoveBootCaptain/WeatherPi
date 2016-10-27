#!/usr/bin/python
# -*- coding: utf-8 -*-
from init_blinkt import *
# import threading


def update_blinkt():

    # threading.Timer(60, update_blinkt).start()

    blink('yellow')

if __name__ == '__main__':

    update_blinkt()
