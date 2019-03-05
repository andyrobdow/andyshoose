# Andy's Hoose

This project makes use of a raspberry pi and a bme280 break out board to create an indoor environment sensing platform. Mwasurements are taken every minute for temperature, humidity and pressure and written to a local csv file. Current values are also sent as a javascript file so that current conditions can be read externally.

### Running Headless Raspberry Pi

The completed script runs using crontab:

        sudo crontab -e

        @reboot python /home/pi/Documents/andyshoose/main.py &

### BME280.py

The project relies heavily on BME280.py by Matt Hawkins, thanks Matt! Get it here: https://www.raspberrypi-spy.co.uk
