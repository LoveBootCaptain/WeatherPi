# these scripts help to run WeatherPi as a linux service

- buttons.sh is for mapping some function to gpio-buttons on the pi
- turnLedsOff.sh turns all leds and addon-boards off at boot and shutdown/reboot
- WeatherPi.sh is the main application and can benefit from the other two services

## make files executable and copy the services

    cd ~/WeatherPi/Modules/

    sudo chmod +x clear.py
    sudo chmod +x init_buttons.py

    cd ..

    sudo chmod +x WeatherPi.py

    cd scripts/

    sudo chmod +x *.sh

    sudo cp *.sh /etc/init.d/

    sudo reboot
    
## test the services    
    
    sudo service WeatherPi start
    sudo service WeatherPi stop
    sudo service WeatherPi restart
    
    sudo service turnLedsOff start
    sudo service turnLedsOff stop
    
    sudo service buttons start
    sudo service buttons stop
    
## start services at boot
    
    sudo update-rc.d turnLedsOff.sh defaults
    sudo update-rc.d buttons.sh defaults
    sudo update-rc.d WeatherPi.sh defaults

## remove services from boot

    sudo update-rc.d turnLedsOff.sh remove
    sudo update-rc.d buttons.sh remove
    sudo update-rc.d WeatherPi.sh remove