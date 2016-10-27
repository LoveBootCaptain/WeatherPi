#!/usr/bin/python
# -*- coding: utf-8 -*-
from Modules.update_latest_weather import *
from Modules.update_matrix import *
from Modules.update_unicorn import *
from Modules.update_io import *
from Modules.update_log import *
from Modules.clear import *


def main():

    threading.Timer(THREADING_TIMER, main).start()

    try:

        update_latest_weather()
        time.sleep(0.5)

        update_log()
        time.sleep(0.5)

        update_matrix()
        update_bargraph()
        time.sleep(0.5)

        update_io_thing_speak()
        time.sleep(0.5)

        update_io_adafruit()
        time.sleep(0.5)

        get_icon_path()
        time.sleep(0.5)

    except (KeyboardInterrupt, AttributeError, Exception, StandardError):

        clear_all()


if __name__ == '__main__':

    try:

        matrix_init()
        unicorn_init()
        blinkt_init()

        update_clock_matrix()

        main()

        update_unicorn()

    except (KeyboardInterrupt, AttributeError, Exception, StandardError):

        clear_all()
