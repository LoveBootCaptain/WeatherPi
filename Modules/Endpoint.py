#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from itertools import izip
from flask import Flask, jsonify, render_template

from Data import Data
from UpdateLog import log_string


class Endpoint(Data):

    def unicorn_pi_data(self):

        log_string('requesting unicorn_pi data')

        rain_forecast = []

        for item in self.hourly_data[:8]:
            rain_percentage = item['precipProbability'] * 100
            rain_forecast.append(int(rain_percentage))

        # response
        unicorn_pi_data = {
            "temp": self.sensor_temp_outside,
            "icon": self.weather_icon,
            "summary": self.forecast,
            "rain_forecast": rain_forecast
        }

        log_string('returned data: {}'.format(unicorn_pi_data))

        return unicorn_pi_data

    def sensor_module_data(self):

        log_string('requesting sensor data')

        # response
        data = {
            "Wohnzimmer": self.sensor_temp_wohnzimmer,
            "Kinderzimmer": self.sensor_temp_kinderzimmer,
            "Schlafzimmer": self.sensor_temp_schlafzimmer,
            "Balkon": self.sensor_temp_outside
        }

        log_string('returned data: {}'.format(data))

        return data

    @staticmethod
    def rpi_stats():

        # cpu stats
        res = os.popen('vcgencmd measure_temp').readline()
        cpu_temp = res.replace("temp=", "").replace("'C\n", "")

        cpu_use = (str(os.popen("TERM=vt100 top -b -n 1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()).replace(',', '.'))

        # ram
        ram_data = os.popen('free')
        ram_line_1 = ram_data.readline().split()
        ram_line_2 = ram_data.readline().split()[1:]
        ram_line_2 = [int(x) for x in ram_line_2]
        ram_line_2 = [int(x / 1024) for x in ram_line_2]

        ram = dict(izip(ram_line_1, ram_line_2))  # dict(zip(ram_line_1, ram_line_2))

        ram_used = int(ram['used'] * 100 / ram['total'])
        ram['used_prec'] = ram_used

        # disk
        disk_data = os.popen("df -m /")
        disk_line_1 = disk_data.readline().replace(
            '1M-Blöcke', 'total').replace(
            'Verw%', 'used_prec').replace(
            'Verf\xc3\xbcgbar', 'free').replace(
            'Benutzt', 'used').split()[1:5]
        disk_line_2 = disk_data.readline().replace('%', '').split()[1:5]
        disk_line_2 = [int(x) for x in disk_line_2]

        disk = dict(izip(disk_line_1, disk_line_2))

        # response
        rpi_stats = {
            "CPU": {
                "temp": float(cpu_temp),
                "usage": float(cpu_use)
            },
            "RAM": ram,
            "DISK": disk
        }

        log_string('returned data: {}'.format(rpi_stats))

        return rpi_stats


app = Flask(__name__)


@app.route('/api/node')
def get_unicorn_pi_data():
    return jsonify(Endpoint().unicorn_pi_data())


@app.route('/api/sensors')
def get_sensor_data():
    return jsonify(Endpoint().sensor_module_data())


@app.route('/api/rpi')
def get_rpi_stats():
    return jsonify(Endpoint().rpi_stats())


@app.route('/')
def index():
    return render_template('childs/home.jinja2')


@app.route('/node')
def node():
    return render_template('childs/node.jinja2', node_data=Endpoint().unicorn_pi_data())


@app.route('/sensors')
def sensors():
    return render_template('childs/sensors.jinja2', sensor_data=Endpoint().sensor_module_data())


@app.route('/rpi')
def rpi():
    return render_template('childs/rpi.jinja2', rpi_data=Endpoint().rpi_stats())


@app.route('/base')
def base():
    return render_template('base.jinja2')


log_string('api endpoints created')


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=4545)

