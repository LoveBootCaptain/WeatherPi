#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from Config import Config
from init_logging import log_string


class Data:
    def __init__(self):

        log_string('Run Update module by: {}'.format(self.__class__))

        # set the configs
        self.config = Config().get_config()

        self.api_path = '/home/pi/WeatherPi/logs/latest_weather.json'
        self.sensor_path = '/home/pi/WeatherPi/logs/sensors.json'
        self.test_path = '/home/pi/WeatherPi/logs/test_weather_with_alarm.json'

        self.api_data = self.json_data(self.api_path)
        self.sensor_data = self.json_data(self.sensor_path)

        # api data
        self.temp_api = self.api_data['currently']['temperature']
        self.rain_percentage_data = self.api_data['currently']['precipProbability']
        self.rain_percentage = self.rain_percentage_data * 100
        self.forecast = self.api_data['currently']['summary'].encode('UTF-8')
        self.weather_icon = self.api_data['currently']['icon']
        self.hourly_data = self.api_data['hourly']['data']
        self.hourly_forecast = self.api_data['hourly']['summary']
        self.daily = self.api_data['daily']['data']
        self.forecast_today = self.daily[0]
        self.temp_range_today_min = int(self.forecast_today['temperatureMin'])
        self.temp_range_today_max = int(self.forecast_today['temperatureMax'])

        # generated string
        self.forecast_today = '{} bis {}°C - {}'.format(
            self.temp_range_today_min,
            self.temp_range_today_max,
            self.hourly_forecast.encode('UTF-8')
        )
        
        # variables for weather icon
        self.version_path = self.config['UNICORN_VERSION'] + '/'
        self.folder_path = '/home/pi/WeatherPi/Modules/Animations/'
        self.path = self.folder_path + self.version_path
        self.icon_extension = '.' + 'png'
        
        self.icon_path = self.path + self.weather_icon + self.icon_extension

        # sensor data base
        self.sensor_base = [item for item in self.sensor_data['devices']
                            if item.get('_id') == self.config['NETATMO_DEVICE_ID']][0]

        # sensor data inside

        self.sensor_temp_inside = self.sensor_base['dashboard_data']['Temperature']
        self.sensor_pressure_inside = self.sensor_base['dashboard_data']['AbsolutePressure']
        self.sensor_humidity_inside = self.sensor_base['dashboard_data']['Humidity']
        
        # sensor data outside
        self.sensor_modules = self.sensor_base['modules']

        self.sensor_modules_outside = [item for item in self.sensor_modules
                                       if item.get('_id') == self.config['NETATMO_SENSOR_ID']][0]

        self.sensor_temp_outside = self.sensor_modules_outside['dashboard_data']['Temperature']
        self.sensor_humidity_outside = self.sensor_modules_outside['dashboard_data']['Humidity']

    def json_data(self, path):
        try:
            print('read data from path: {}'.format(path))

            data = open(path).read()
            json_data = json.loads(data)

            return json_data
        except IOError:

            log_string('ERROR - file read by module'.format(self.__class__))


if __name__ == '__main__':
    print(Data().sensor_temp_outside)


# # api data
# self.temp_api = self.json_data['currently']['temperature']
# self.rain_percentage_data = self.json_data['currently']['precipProbability']
# self.rain_percentage = self.rain_percentage_data * 100
# self.forecast = self.json_data['currently']['summary'].encode('UTF-8')
# self.weather_icon = self.json_data['currently']['icon']
# self.hourly_data = self.json_data['hourly']['data']
# self.hourly_forecast = self.json_data['hourly']['summary']
# self.daily = self.json_data['daily']['data']
# self.forecast_today = self.daily[0]
# self.temp_range_today_min = int(self.forecast_today['temperatureMin'])
# self.temp_range_today_max = int(self.forecast_today['temperatureMax'])
#
# # generated string
# self.forecast_today = '{} bis {}°C - {}'.format(
#     self.temp_range_today_min,
#     self.temp_range_today_max,
#     self.hourly_forecast.encode('UTF-8')
# )
#
# self.icon_path = self.path + self.weather_icon + self.icon_extension

# self.sensor_temp_outside = self.json_data['currently']['sensor_temp_outside']
# self.sensor_temp_inside = self.json_data['currently']['sensor_temp_inside']
# self.sensor_pressure_outside = self.json_data['currently']['sensor_pressure_outside']
# self.sensor_humidity_outside = self.json_data['currently']['sensor_humidity_outside']
# self.sensor_pressure_inside = self.json_data['currently']['sensor_pressure_inside']
# self.sensor_humidity_inside = self.json_data['currently']['sensor_humidity_inside']


# # variables for weather icon
# self.version_path = self.config['UNICORN_VERSION'] + '/'
# self.folder_path = '/home/pi/WeatherPi/Modules/Animations/'
# self.path = self.folder_path + self.version_path
# self.icon_extension = '.' + 'png'

# #  get sensor data inside
# sensor_temp_inside = 0
# log_string('fetched sensortempinside from adafruit.io: {}'.format(sensor_temp_inside))
#
# sensor_pressure_inside = 0
# log_string('fetched sensorpressureinside from adafruit.io: {}'.format(sensor_pressure_inside))
#
# sensor_humidity_inside = 0
# log_string('fetched sensorhumidityinside from adafruit.io: {}'.format(sensor_humidity_inside))
#
# #  get sensor data outside
# sensor_temp_outside = 0
# log_string('fetched sensortempoutside from adafruit.io: {}'.format(sensor_temp_outside))
#
# sensor_pressure_outside = 0
# log_string('fetched sensorpressureoutside from adafruit.io: {}'.format(sensor_pressure_outside))
#
# sensor_humidity_outside = 0
# log_string('fetched sensorhumidityoutside from adafruit.io: {}'.format(sensor_humidity_outside))
#
# blink('blue')
#
# # add data to data dict
# self.data['currently']['sensor_temp_inside'] = sensor_temp_inside
# self.data['currently']['sensor_pressure_inside'] = sensor_pressure_inside
# self.data['currently']['sensor_humidity_inside'] = sensor_humidity_inside
#
# log_string('added sensor data to temporary json data: '
#            'temp. inside:{} - humidity inside: {} - pressure inside: {}'.format(
#                 sensor_temp_inside,
#                 sensor_humidity_inside,
#                 sensor_pressure_inside
#             ))
#
# self.data['currently']['sensor_temp_outside'] = sensor_temp_outside
# self.data['currently']['sensor_pressure_outside'] = sensor_pressure_outside
# self.data['currently']['sensor_humidity_outside'] = sensor_humidity_outside
#
# log_string('added sensor data to temporary json data: '
#            'temp. outside:{} - humidity outside: {} - pressure outside: {}'.format(
#                 sensor_temp_outside,
#                 sensor_humidity_outside,
#                 sensor_pressure_outside
#             ))
#
#
# forecast = RainData()
#
# small_json = {
#
#     "temp_api": self.temp_api,
#     "temp_in": self.sensor_temp_inside,
#     "temp_out": self.sensor_temp_outside,
#     "icon": self.weather_icon,
#     "summary": self.forecast,
#     "rain_probability": self.rain_percentage,
#     "rain_forecast": forecast.rain_forecast()
#
# }
#
# print(small_json)
#
# with open('/home/pi/WeatherPi/logs/small_weather.json', 'w') as outputfile:
#     json.dump(small_json, outputfile, indent=2, sort_keys=True)