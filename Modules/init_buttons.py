#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

import RPi.GPIO as GPIO

from init_logging import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def start_service(start):

    log_string('Button pressed:{}\n'
               'start WeatherPi service'.format(start))

    os.system('sudo systemctl stop WeatherPi.service')
    os.system('sudo systemctl start WeatherPi.service')


def stop_service(stop):

    log_string('Button pressed:{}\n'
               'stop WeatherPi service'.format(stop))

    os.system('sudo systemctl stop WeatherPi.service')


def restart_service(restart):

    log_string('Button pressed:{}\n'
               'restart WeatherPi service'.format(restart))

    os.system('sudo systemctl stop WeatherPi.service')
    os.system('sudo systemctl restart WeatherPi.service')


def shutdown_service(shutdown):
    log_string('Button pressed:{}\n'
               'shutdown Pi'.format(shutdown))

    os.system('sudo shutdown now')


def reboot_service(reboot):
    log_string('Button pressed:{}\n'
               'reboot Pi'.format(reboot))

    os.system('sudo shutdown -r now')


GPIO.add_event_detect(22, GPIO.FALLING, callback=restart_service, bouncetime=1000)
GPIO.add_event_detect(27, GPIO.FALLING, callback=stop_service, bouncetime=1000)
GPIO.add_event_detect(17, GPIO.FALLING, callback=shutdown_service, bouncetime=1000)

if __name__ == '__main__':

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        os.system('sudo service WeatherPi stop')
        GPIO.cleanup()
