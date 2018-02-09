#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template

from multiprocessing import Process
from init_logging import log_string
from Endpoint import Endpoint

app = Flask(__name__)


class WebApp(Process):
    name = "Flask WebApp Process"

    def __init__(self):
        Process.__init__(self)
        self.app = app
        self.daemon = True

    def run(self):
        self.app.run(debug=True, host='0.0.0.0', port=4545)


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
    return render_template('home.html')


@app.route('/node')
def node():
    return render_template('node.html', node_data=Endpoint().unicorn_pi_data())


@app.route('/sensors')
def sensors():
    return render_template('sensors.html', sensor_data=Endpoint().sensor_module_data())


@app.route('/rpi')
def rpi():
    return render_template('rpi.html', rpi_data=Endpoint().rpi_stats())


# @app.route('/base')
# def base():
#     blink('yellow')
#     return render_template('base.html')


log_string('api endpoints created')


if __name__ == '__main__':

    WebApp().run()


