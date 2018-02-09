#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
import pytz
import tzlocal

from itertools import izip

from Data import Data
from UpdateLog import log_string


class Endpoint(Data):

    def node_data(self):
        log_string('requesting node data')

        rain_forecast = []

        for item in self.hourly_data[:8]:
            rain_percentage = item['precipProbability'] * 100
            rain_forecast.append(int(rain_percentage))

        time_str = datetime.fromtimestamp(int(self.api_time)).strftime('%H:%M:%S')

        # response
        node_data = {
                "temp": self.sensor_temp_outside,
                "icon": self.weather_icon,
                "summary": self.forecast,
                "rain_forecast": rain_forecast,
                "updated": time_str
            }

        log_string('returned data: {}'.format(node_data))

        return node_data

    def sensor_module_data(self):
        log_string('requesting sensor data')

        wohnzimmer = self.sensor_base['dashboard_data']
        kinderzimmer = self.sensor_kinderzimmer['dashboard_data']
        schlafzimmer = self.sensor_schlafzimmer['dashboard_data']
        balkon = self.sensor_outside['dashboard_data']

        def get_updated_time(sensor_time):

            update_time = datetime.utcfromtimestamp(sensor_time)
            local_time = datetime.utcnow()
            last_update_time = int((local_time - update_time).seconds / 60)

            return last_update_time

        # response
        data = {
            "Wohnzimmer": {
                "Temperatur": wohnzimmer['Temperature'],
                "Luftdruck": wohnzimmer['Pressure'],
                "Kohlendioxyd": wohnzimmer['CO2'],
                "Luftfeuchtigkeit": wohnzimmer['Humidity'],
                "Lautstärke": wohnzimmer['Noise'],
                "Updated": get_updated_time(wohnzimmer['time_utc'])
            },
            "Kinderzimmer": {
                "Temperatur": kinderzimmer['Temperature'],
                "Kohlendioxyd": kinderzimmer['CO2'],
                "Luftfeuchtigkeit": kinderzimmer['Humidity'],
                "Updated": get_updated_time(kinderzimmer['time_utc'])
            },
            "Schlafzimmer": {
                "Temperatur": schlafzimmer['Temperature'],
                "Kohlendioxyd": schlafzimmer['CO2'],
                "Luftfeuchtigkeit": schlafzimmer['Humidity'],
                "Updated": get_updated_time(schlafzimmer['time_utc'])
            },
            "Balkon": {
                "Temperatur": balkon['Temperature'],
                "Luftfeuchtigkeit": balkon['Humidity'],
                "Updated": get_updated_time(balkon['time_utc'])
            }
        }

        log_string('returned data: {}'.format(data))

        return data

    @staticmethod
    def rpi_stats():
        # cpu stats
        res = os.popen('vcgencmd measure_temp').readline()
        cpu_temp = res.replace("temp=", "").replace("'C\n", "")

        cpu_use = (
        str(os.popen("TERM=vt100 top -b -n 1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()).replace(',', '.'))

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

        time_str = datetime.now().strftime('%H:%M:%S')

        # response
        rpi_stats = {
            "CPU": {
                "temp": float(cpu_temp),
                "usage": float(cpu_use)
            },
            "RAM": ram,
            "DISK": disk,
            "updated": time_str
        }

        log_string('returned data: {}'.format(rpi_stats))

        return rpi_stats
