#!/usr/bin/python
# -*- coding: utf-8 -*-
from Modules.update_latest_weather import *
from Modules.update_matrix import *
from Modules.update_unicorn import *
from Modules.update_io import *
from Modules.update_log import *
from Modules.clear import *


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

    except KeyboardInterrupt:
        
        quit_all()
        clear_all()


if __name__ == '__main__':

    try:

        RUNNING = True

        matrix_init()
        unicorn_init()
        blinkt_init()

        update_clock_matrix()

        main()

        update_unicorn()

    except KeyboardInterrupt:

        RUNNING = False

        quit_all()
        clear_all()
