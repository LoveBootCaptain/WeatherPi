#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from collections import namedtuple
from datetime import datetime

from Data import Data
from init_logging import log_string

TFM = '%d.%m.%Y %H:%M:%S'


def time_convert(time_stamp):
    return str(datetime.fromtimestamp(int(time_stamp)).strftime(TFM))


def check_alarms():

    weather = Data().api_data

    alarms = {}

    try:

        alarm_weather = weather['alerts']

        Alarm = namedtuple('Alarm', ['severity', 'title', 'start_time', 'expires', 'duration', 'lasts', 'description'])

        for idx, alarm_obj in enumerate(alarm_weather):

            severity, title, time_start, expires, description = alarm_obj['severity'], alarm_obj['title'], \
                                                                alarm_obj['time'], alarm_obj['expires'], \
                                                                alarm_obj['description'].encode('UTF-8')

            alarm_start_time = time_convert(int(time_start))
            alarm_expire_time = time_convert(int(expires))
            alarm_duration = str(datetime.fromtimestamp(expires) - datetime.fromtimestamp(time_start))

            alarm_lasts = (datetime.fromtimestamp(expires) - datetime.fromtimestamp(time.time())).seconds / 60.0 / 60.0

            alarm_lasts = int(round(alarm_lasts, 0))

            alarm = Alarm(str(severity), str(title),
                          alarm_start_time, alarm_expire_time, alarm_duration, alarm_lasts,
                          str(description))

            if alarm.severity == 'warning':

                log_string('warning Alarm: {}'.format(alarm))
                alarms[idx] = {'severity': alarm.severity, 'duration': alarm_lasts}

            elif alarm.severity == 'watch':

                log_string('watch Alarm: {}'.format(alarm))
                alarms[idx] = {'severity': alarm.severity, 'duration': alarm_lasts}

            elif alarm.severity == 'advisory':

                log_string('watch Alarm: {}'.format(alarm))
                alarms[idx] = {'severity': alarm.severity, 'duration': alarm_lasts}

            else:
                alarms = None

        log_string('Alle Wetter Alarme: {}'.format(alarms))
        return alarms

    except KeyError:

        log_string('no weather alerts')
        return None


if __name__ == '__main__':

    check_alarms()
