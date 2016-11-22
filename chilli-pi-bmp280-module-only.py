#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  chilli-pi-bmp280-module-only.py
#  
#  Copyright 2016  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

##### CHILLI-PI MONITORING SYSTEM - BMP280 TEMPERATURE/PRESSURE MODULE #####

# Simple test of reading the ambient temperature and pressure data from the BMP280.
# Prints to the console and uploads to the Adafruit IO site.
# Based upon original code written by: Adafruit
# Adapted for Chilli-Pi: Paul Clarke 2016.

###################################
# FURTHER WORK                    #
# - add sensor average over time? #
# - add sensor de-bounce?         #
# - add alarm setpoints           #
# - add LED alarm trigger         #
# - add config file               #
# - add time period to poll data  #
###################################

# Import required modules.

import time					# 'time' allows our Raspberry Pi to define time, and enables the use of time periods in the code.
from Adafruit_IO import *		# 'Adafruit_IO' allows us to use the cloud based Adafruit dashboard system.
from Adafruit_BME280 import *	# 'Adafruit_BME280 allows us to access the BMP280 ambient pressure and temperature sensor package.

##############################################################
# This section to be used for handling a simple config file. #
# Uncomment to make live.                                    #
# ***CURRENTLY NOT USED - KEEP COMMENTED UNTIL READY***      #
# Handle a simple configuration file:                        #
# config = ConfigParser.RawConfigParser()                    #
# config.read('chilli-pi.cfg')                               #
# chilli_pin = config.getint('sensors', 'name1_pin')         #
# pir_pin = config.getint('sensors', 'name2_pin')            #
##############################################################

# Create a BMP280 instance.

sensor = BME280(mode=BME280_OSAMPLE_8)

# Adding ANSI escape codes to provide colour coding of data in the console.
# Source - # https://computers.tutsplus.com/tutorials/build-a-raspberry-pi-moisture-sensor-to-monitor-your-plants--mac-52875

# All ANSI escape codes start with '\x1b[' followed by the particular instruction code.

PREVIOUS_1_LINE = "\x1b[1F"	# nF = Moves cursor to beginning of the line 'n' lines up.
RED_BACK = "\x1b[41;37m"	# Set background colour.
GREEN_BACK = "\x1b[42;30m"	# Set background colour.
YELLOW_BACK = "\x1b[43;30m"	# Set background colour.
RESET = "\x1b[0m"			# Set SGR (select graphic rendition) to '0m' (reset/normal)
NEXT_LINE = "\x1b[0E"		# nE = Moves cursor to beginning of the line 'n' lines down.
HIDE_CURSOR = "\x1b[?25l"	# Hide the cursor.

# Set up the look of the console.

print '\x1b[2J\x1b[H'											# Clear the screen and put the cursor at the top.
print 'CHILLI-PI MONITORING SYSTEM - BMP280 MODULE'				# Print title.
print ('=' * 43) + '\n'											# Print title divider character times the number needed.
print ('Reading BMP280 channels, press Ctrl-C to quit...\n')	# Print info.
print ('| {a:^6} | {b:^9} | {c:^6} | {d:^6} |'.format(a='Temp.C', b='Press.P', c='Press.H', d='Temp.F'))	# Print nice channel column headers.
print ('-' * 41)	

# Read data function.

def read_bmp280_data():
	"Function to read ambient temperature / pressure data from the BMP280 PCB"
	bmp280_temp_c = sensor.read_temperature()
	bmp280_pascals = sensor.read_pressure()
	
	# Convert data to other useful measurements scales.
	
	bmp280_hectopascals = bmp280_pascals / 100 				# Convert pressure from pascals to hectopascals.
	bmp280_temp_f = bmp280_temp_c * 9.0 / 5.0 + 32.0		# Convert temperature from celsius to fahrenheit.

	return bmp280_temp_c, bmp280_pascals, bmp280_hectopascals, bmp280_temp_f

while True:
	temp_c, press_p, press_h, temp_f = read_bmp280_data() 	# Unpack the values from the read_bmp280_data function.
	
	# Print the data values to the console using ANSI escape codes.
	
	print('| {0:^6.2f} | {1:^6.2f} | {2:^6.2f} | {3:^6.2f} |'.format(temp_c, press_p, press_h, temp_f)) + PREVIOUS_1_LINE + RESET + HIDE_CURSOR
	
	#{:.1f}
	
	aio = Client('5b7efbea2e154aedb80e75564d482fd9') # Log into Adafruit IO.
	
	# Send data out to the Adafruit IO site using 'aio.send('feed_name', data_value)'.
	
	aio.send('bmp280_data_temp_c', temp_c)
	aio.send('bmp280_data_press_p', press_p)
	aio.send('bmp280_data_press_h', press_h)
	aio.send('bmp280_data_temp_f', temp_f)
	
	time.sleep(1) #Sleep before taking another reading. Value is in seconds, 60=1min, 3600=1hour.
