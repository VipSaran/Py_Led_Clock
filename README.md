# Py LED Clock

A simple clock & temperature application in Python for a [7-segment LED backpack](https://learn.adafruit.com/adafruit-led-backpack/0-dot-56-seven-segment-backpack) connected to Raspberry Pi.

The app relies on LED [libraries from Adafruit](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code), but uses own, slightly modified/extended files.


## Initial Configuration

### I2C Address

In `clock.py` change the I2C address to the one you will be using (if it's different than mine: `0x77`).

### Daylight (sunrise/sunset) Zone

The application dims the display during the night and brightens it while in daylight, so in `clock.py` change the value of `city_name` to best correspond to your time zone. See [Astral documentation](http://pythonhosted.org/astral/#cities) for list of supported cities.

### Weather Information

The city temperature is read from [forecast.io](https://developer.forecast.io/docs/v2) weather API. For that you need to specify `APIKey`, `LATITUDE` and `LONGITUDE` values in `clock.py`. To keep the API usage in the free range (so, under 1000 requests/day), the weather info is refreshed only every 2 minutes. Change this if you have a paid forecast.io API license.

Temperature will be displayed in degrees Celsius unless `FAHRENHEIT` is set to `True`.


### Script Location

In `led_clock` file (the one used for service) change the `APP_HOME` value to correspond to the directory you have cloned this project into and where `clock.py` is run from.

## Installation

## Setting up LED clock as service

Even though the program can be run directly (from command line), it is of better use if it automatically boots up with the system. To do so, simply install it as a service:

    sudo cp led_clock /etc/init.d/
    sudo chmod +x /etc/init.d/led_clock
    sudo update-rc.d led_clock defaults

## Installing dependencies

The *Py LED Clock* program uses some 3rd party modules. First prepare the environment (if not already done) for easy module installation:

    sudo apt-get install python-pip
    sudo apt-get install python-dev
    sudo apt-get install python-smbus

Then install the actual modules:

    sudo pip install rpi.gpio
    sudo pip install requests
    sudo pip install astral
    sudo pip install pytz


## Running

To run the service, execute `sudo /etc/init.d/led_clock start`. Additionally, the service will run automatically after a reboot.


## Notes

Because of display size limitation, both Celsius and Fahrenheit degree symbols for *negative* temperature values are displayed as 'E' (should be read as 'C -' for Celsius and 'F -' for Fahrenheit). 

If you encounter an error like: `/etc/init.d/led_clock: 20: /etc/init.d/led_clock: /home/pi/python/led/clock.py: not found`, change the line endings Windows --> Unix.


## License

    Copyright 2015 Robert Šarić

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.