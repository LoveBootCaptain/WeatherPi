#!/usr/bin/python
# -*- coding: utf-8 -*-
from init_io import *


# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0


def sensor_inside_init():

    try:

        sensor_temp_inside = aio_sensors.receive('sensortempinside')
        sensor_temp_inside = float(sensor_temp_inside.value)

        sensor_pressure_inside = aio_sensors.receive('sensorpressureoutside')
        sensor_pressure_inside = float(sensor_pressure_inside.value)

        sensor_humidity_inside = aio_sensors.receive('sensorhumidityoutside')
        sensor_humidity_inside = float(sensor_humidity_inside.value)

        log_string('Temperature Inside        :   {0:0.3f}°C / {1:0.3F}°F'.format(sensor_temp_inside,
                                                                                  c_to_f(sensor_temp_inside)))
        log_string('Sensor Pressure Inside    :   {0:0.2f} hPa'.format(sensor_pressure_inside))

        log_string('Sensor Humidity Inside    :   {0:0.2f} %'.format(sensor_humidity_inside))

    except IOError:

        log_string('ERROR - sensor_inside_init')


def sensor_outside_init():

    try:

        sensor_temp_outside = aio_sensors.receive('sensortempoutside')
        sensor_temp_outside = float(sensor_temp_outside.value)

        sensor_pressure_outside = aio_sensors.receive('sensorpressureoutside')
        sensor_pressure_outside = float(sensor_pressure_outside.value)

        sensor_humidity_outside = aio_sensors.receive('sensorhumidityoutside')
        sensor_humidity_outside = float(sensor_humidity_outside.value)

        log_string('Temperature Outside       :   {0:0.3f}°C / {1:0.3F}°F'.format(sensor_temp_outside,
                                                                                  c_to_f(sensor_temp_outside)))
        log_string('Sensor Pressure Outside   :   {0:0.2f} hPa'.format(sensor_pressure_outside))

        log_string('Sensor Humidity Outside   :   {0:0.2f} %'.format(sensor_humidity_outside))

    except IOError:

        log_string('ERROR - sensor_outside_init')

if __name__ == '__main__':

    try:

        sensor_inside_init()
        sensor_outside_init()

    except KeyboardInterrupt:
        from clear import *
        clear_all()
