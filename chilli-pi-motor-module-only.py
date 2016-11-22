#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  chilli-pi-digital-moisture-sensor-module
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

######################

# Basic code to read from a digital output moisture sensor with Python.
# Based upon original code written by: ModMyPi - git://github.com/modmypi/Moisture-Sensor
# Adapted for Chilli-Pi: Paul Clarke 2016.

# Import required modules;

import os 						# 'os' allows us to enable our 1-Wire drivers and interface with the sensor.
import time					# 'time' allows our Raspberry Pi to define time, and enables the use of time periods in the code.
import RPi.GPIO as GPIO 		# 'RPi.GPIO' allows us to use the GPIO pins on the Raspberry Pi for the moisture sensor.
from Adafruit_IO import Client	# 'Adafruit_IO' allows us to use the cloud based Adafruit dashboard system.

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

# GPIO setup 

GPIO.setmode(GPIO.BCM)								# Set our GPIO numbering mode to BCM.
digital_moisture_sensor_pin = 17					# Set the GPIO pin that the digital moisture sensor is connected to.
led_pin = 27										# Set the GPIO pin that the testing LED is connected to.
GPIO.setup(digital_moisture_sensor_pin, GPIO.IN) 	# Set the GPIO pin to be an input.
GPIO.setup(led_pin, GPIO.OUT)						# Set the GPIO pin to be an output.

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

# Check the variable from the previous function for any errors.
# Line0 in the file is for error checking (crc = cyclic redundancy check), Line1 in the file is the temperature 't'.
# Strip the line0 except for the last three digits, and check for the “YES” signal which is a successful sensor reading.
# In Python, not-equal is defined as “!=”, while the reading does not equal YES, sleep for 0.2s and repeat.

# This is the callback function for the digital output signal from the moisture sensor.
# This function will be called every time there is a change on the specified GPIO pin.

def callback(digital_moisture_sensor_pin):  
	if GPIO.input(digital_moisture_sensor_pin):
		DSMS = 0#print message # PCB LED off, soil is dry.
		#sendEmail(message_dead) #Currently not used.
	else:
		DSMS = 1#print message # PCB LED on, soil is wet.
		#sendEmail(message_alive) #Currently not used.

# Watch the digital soil moisture pin and declare when the pin goes HIGH or LOW.
GPIO.add_event_detect(digital_moisture_sensor_pin, GPIO.BOTH, bouncetime=300)

# Assign a function to the digital soil moisture pin, so that when the previous line tells us there is a change on the pin, run this function.
GPIO.add_event_callback(digital_moisture_sensor_pin, callback)


# Define a function to read the data from the BMP280 sensor package and assign to variables.

def read_bmp280():
	bmp280_temp_c = sensor.read_temperature()
	bmp280_pascals = sensor.read_pressure()
	
	# Convert to standard measurements.
	bmp280_hectopascals = bmp280_pascals / 100
	bmp280_temp_f = bmp280_temp_c * 9.0 / 5.0 + 32.0
	return bmp280_temp_c, bmp280_pascals, bmp280_hectopascals, bmp280_temp_f

# Clear the screen and put the cursor at the top.

print '\x1b[2J\x1b[H'
print 'CHILLI-PI MONITORING SYSTEM - DIGITAL MOISTURE SENSOR MODULE'
print ('=' * 43) + '\n'											# Print title divider character times the number needed.
print ('Reading  digital moisture channel, press Ctrl-C to quit...\n')	# Print info.
print ('| {a:^13} |'.format(a='Dig.Moisture'))					# Print nice channel column headers.
print ('-' * 17)												# Print column header divider.

# Loop the process and output the temperature data every 1 second.
# {:>10} is used to align right.
# {:.2f} is used for decimal precision

while True:
		
	# Set background colour indicators for digital moisture sensor output.
		
	if GPIO.input(digital_moisture_sensor_pin):
		GPIO.output(led_pin, True)
		dig_soil_moisture_background = RED_BACK
		print dig_soil_moisture_background + "| Status: ALERT |" + PREVIOUS_1_LINE + RESET + HIDE_CURSOR
	else:
		GPIO.output(led_pin, False)
		dig_soil_moisture_background = GREEN_BACK
		print dig_soil_moisture_background + "|  Status: OK   |" + PREVIOUS_1_LINE + RESET + HIDE_CURSOR
	
	aio = Client('5b7efbea2e154aedb80e75564d482fd9') # Log into Adafruit IO.
	
	# Send data out to the Adafruit IO site using 'aio.send('feed_name', data_value)'.
	
	aio.send('dig_moisture_sensor', digital_moisture_sensor_pin)
	
	time.sleep(1) #Sleep before taking another reading. Value is in seconds, 60=1min, 3600=1hour.
