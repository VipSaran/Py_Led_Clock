#!/usr/bin/python

import logging
import math
import requests
import signal
import sys
import time
import datetime
from Adafruit_7Segment import SevenSegment
from astral import Astral

segment = SevenSegment(address=0x77)

FORMAT = '%(asctime)-15s %(levelname)s:%(message)s'
logging.basicConfig(
    format=FORMAT, filename='log/clock.err', level=logging.ERROR)
    # format=FORMAT, filename='log/clock.log', level=logging.DEBUG)


def receive_signal(signal, frame):
    logging.debug('received signal: %s', signal)
    segment.clear()
    sys.exit(0)


signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)

brightness = -1
BRIGHTNESS_DAY = 10
BRIGHTNESS_NIGHT = 0
brightness_checked_at = time.time() - 700
daytime = False

temp_city = 0

# forecast.io configuration
APIKey = ''
LATITUDE = ''
LONGITUDE = ''
FAHRENHEIT = False

city_name = ''
a = Astral()
a.solar_depression = 'civil'
city = a[city_name]


def is_daytime(now):
    result = True
    try:
        sun = city.sun(date=now, local=True)

        sun_start = sun['sunrise']
        sun_end = sun['sunset']
        logging.debug("Sunrise: %s; Sunset: %s" % (sun_start, sun_end))

        b_daytime_start = now.hour > sun_start.hour or (
            now.hour == sun_start.hour and now.minute > sun_start.minute)
        b_daytime_end = now.hour < sun_end.hour or (
            now.hour == sun_end.hour and now.minute < sun_end.minute)

        logging.debug("b_daytime_start: %s; b_daytime_end: %s" %
                      (b_daytime_start, b_daytime_end))

        result = b_daytime_start and b_daytime_end
    except Exception, e:
        logging.error('Exception (astral): %s', e)

    return result


updated_s = -1

# Continually update the time on a 4 char, 7-segment display
while(True):
    now = datetime.datetime.now()
    logging.debug('now: %s', now.strftime("%s"))

    hour = now.hour
    minute = now.minute
    second = now.second
    second_09 = second % 10
    dot = False

    if (time.time() > brightness_checked_at + 600):
        brightness_checked_at = time.time()
        logging.debug('brightness_checked_at: %s', brightness_checked_at)

        daytime = is_daytime(now)

    if (daytime):
        if (brightness != BRIGHTNESS_DAY):
            brightness = BRIGHTNESS_DAY
            segment.setBrightness(brightness)
    else:
        if (brightness != BRIGHTNESS_NIGHT):
            brightness = BRIGHTNESS_NIGHT
            segment.setBrightness(brightness)

    if (temp_city == 0 or updated_s < 0 or (updated_s + 120) <= int(now.strftime("%s"))):
        try:
            URL = 'https://api.forecast.io/forecast/' + APIKey + '/' + LATITUDE + \
                ',' + LONGITUDE + '?exclude=minutely,hourly,daily,flags,alerts'
            forecast = requests.get(URL).json()
            logging.debug('forecast: %s', forecast)
            
            temp_city = round(float(forecast["currently"]["temperature"]), 1)
            if (not FAHRENHEIT):
                temp_city = round((temp_city - 32) * 5 / 9, 1)
            logging.debug('Living room temperature: %s %s' %
                          (temp_city, 'F' if FAHRENHEIT else 'C'))

            # if failed requests are counted for daily limit, move this to be updated before the request is made
            updated_s = int(now.strftime("%s"))
            logging.debug('updated_s: %s', updated_s)
            
        except Exception, e:
            logging.error('Exception (temp): %s', e)

    if (temp_city == 0 or second_09 <= 6):
        dot = False
        hour_tens = int(hour / 10)
        hour_ones = hour % 10
        min_tens = int(minute / 10)
        min_ones = minute % 10
    else:
        dot = True
        # show temp if available
        negative_temp = temp_city < 0
        m_floor = math.floor(abs(temp_city))
        logging.debug('m_floor: %s', m_floor)

        hour_tens = int(m_floor / 10)
        logging.debug('hour_tens: %s', hour_tens)

        hour_ones = int(m_floor % 10)
        logging.debug('hour_ones: %s', hour_ones)

        min_tens = int("%.0f" % ((abs(temp_city) - m_floor) * 10))
        logging.debug('min_tens: %s', min_tens)

        if (negative_temp):
            min_ones = 0xE
        else:
            if (FAHRENHEIT):
                min_ones = 0xF
            else:
                min_ones = 0xC

    # Set hours
    segment.writeDigit(0, hour_tens)  # Tens
    segment.writeDigit(1, hour_ones, dot)  # Ones
    # Set minutes
    segment.writeDigit(3, min_tens)  # Tens
    segment.writeDigit(4, min_ones)  # Ones
    # Toggle colon
    segment.setColon(not dot and second % 2)  # Toggle colon at 1Hz
    # Wait one second
    time.sleep(1)
