#!/bin/bash
LED_PID=`ps auxwww | grep clock.py | grep -v grep | head -1 | awk '{print $2}'`
kill -USR1 $LED_PID
