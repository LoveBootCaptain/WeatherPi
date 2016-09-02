#!/bin/sh
### BEGIN INIT INFO
# Provides:          turnLedsOff
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: turnLedsOff
# Description:       turnLedsOff
### END INIT INFO

case "$1" in

    start)
    /usr/bin/sudo /usr/bin/python /home/pi/WeatherPi/Modules/clear.py
    ;;

    stop)
    /usr/bin/sudo /usr/bin/python /home/pi/WeatherPi/Modules/clear.py
    ;;

esac
exit 0
