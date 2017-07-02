#!/usr/bin/python
# -*- coding: utf-8 -*-
from Modules.update_io import *
from Modules.update_latest_weather import *
from Modules.update_log import *
from Modules.update_matrix import *
from Modules.update_unicorn import *


def quit_all():

    for thread in threads:
        thread.cancel()
        thread.join()


def main():

    main_thread = threading.Timer(THREADING_TIMER, main)

    main_thread.start()

    threads.append(main_thread)

    try:

        update_latest_weather()
        update_log()
        update_matrix()
        update_bargraph()
        update_io_thing_speak()
        update_io_adafruit()
        get_icon_path()

    except KeyboardInterrupt:
        
        quit_all()
        clear_all()


if __name__ == '__main__':

    try:

        matrix_init()
        unicorn_init()
        blinkt_init()

        draw_single_icon('raspberry_boot')

        update_clock_matrix()

        main()

        update_unicorn()

    except KeyboardInterrupt:

        quit_all()
        clear_all()
