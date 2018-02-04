#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify

from Data import Data
from UpdateLog import log_string


class Endpoint(Data):

    def unicorn_pi_data(self):

        log_string('requesting unicorn_pi data')

        rain_forecast = []

        for item in self.hourly_data[:8]:
            rain_percentage = item['precipProbability'] * 100
            rain_forecast.append(round(rain_percentage))

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

        data = {
            "Wohnzimmer": self.sensor_temp_wohnzimmer,
            "Kinderzimmer": self.sensor_temp_kinderzimmer,
            "Schlafzimmer": self.sensor_temp_schlafzimmer,
            "Balkon": self.sensor_temp_outside
        }

        log_string('returned data: {}'.format(data))

        return data


app = Flask(__name__)


@app.route('/api/unicorn_pi_data')
def get_unicorn_pi_data():
    return jsonify(Endpoint().unicorn_pi_data())


@app.route('/api/sensors')
def get_sensor_data():
    return jsonify(Endpoint().sensor_module_data())


log_string('api endpoints created')


if __name__ == '__main__':

    log_string('starting rest api')
    app.run(debug=True, host='0.0.0.0', port=4545)

