#!/usr/bin/python
# -*- coding: utf-8 -*-
from multiprocessing import Process
import os

from Modules.Update import Update
from Modules.UpdateLog import UpdateLog
from Modules.UpdateUnicorn import UniCorn, UpdateIcon
from Modules.init_unicorn import unicorn_init
from Modules.update_matrix import *

processes_bar = []


def quit_all():

    for thread in threads:
        thread.cancel()
        thread.join()


def main():

    main_thread = threading.Timer(THREADING_TIMER, main)

    main_thread.start()

    threads.append(main_thread)

    try:

        Update().update_json()

        UpdateLog().create_log()

        update_matrix()

        p = Process(target=update_bargraph)

        for process in processes_bar:
            process.terminate()

        p.start()
        processes_bar.append(p)

        UpdateIcon().set_icon_path()

    except KeyboardInterrupt:
        
        quit_all()
        clear_all()


if __name__ == '__main__':

    Update().update_json()
    os.system('Modules/WebApp.py &')

    try:

        matrix_init()
        unicorn_init()
        blinkt_init()

        UniCorn().draw_single_icon('raspberry_boot')

        update_clock_matrix()

        main()

        UniCorn().update_unicorn()

    except KeyboardInterrupt:

        quit_all()
        clear_all()
