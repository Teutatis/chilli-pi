#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  chilli-pi-adc-module-only.py
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
#  MA 02110-1301, USA

##### CHILLI-PI MONITORING SYSTEM - ADC MODULE #####

# Simple test of reading each analog input from the ADS1x15 and printing it to the screen.
# Based upon original code written by: Tony DiCola.
# Adapted for Chilli-Pi: Paul Clarke 2016.

###################################
# FURTHER WORK                    #
# - add sensor average over time? #
# - add sensor de-bounce?         #
# - add alarm setpoints           #
# - add LED alarm trigger         #
# - add config file               #
###################################

# Import required modules.

import time
import Adafruit_ADS1x15
from Adafruit_IO import Client

# Create an ADS1015 ADC (12-bit) instance.
# NOTE you can change the I2C address from its default (0x48), and/or the I2C bus by passing in these optional parameters:
# adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
# The ADDR pin on the PCB should be set from the datasheet.

adc = Adafruit_ADS1x15.ADS1015()

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.

GAIN = 2 # Current gain value.

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

print '\x1b[2J\x1b[H'												# Clear the screen and put the cursor at the top.
print 'CHILLI-PI MONITORING SYSTEM - LDR MODULE'					# Print title.
print ('=' * 40) + '\n'												# Print title divider character multiplied by the number needed.
print('Reading ADS1015 channels, press Ctrl-C to quit...\n')		# Print info.
print('| {0:^6} | {1:^6} | {2:^6} | {3:^6} |'.format(*range(4))) 	# Print nice channel column headers.
print('-' * 37)

# Read data function.

def read_ads1015_data():
	"Function to read data from the ADS1015 analogue to digital convertor PCB"
	# Set up a list called 'values' that contains '0', four times. e.g. '0, 0, 0, 0'.
	values = [0]*4
	# Loop 4 times, each time reading a channel.
	for i in range(4):
		values[i] = adc.read_adc(i, gain=GAIN)
	next;
	return(values)

while True:
	ch0, ch1, ch2, ch3 = read_ads1015_data() # Unpack the values from the read_ads1015_data function.
	
	# Print the data values to the console using ANSI escape codes.
	
	print('| {0:^6} | {1:^6} | {2:^6} | {3:^6} |'.format(ch0, ch1, ch2, ch3)) + PREVIOUS_1_LINE + RESET + HIDE_CURSOR
	
	aio = Client('5b7efbea2e154aedb80e75564d482fd9') # Log into Adafruit IO.
	
	aio.send('ads1015_data_ch0', ch0)  # Send data out to the Adafruit IO site using 'aio.send('feed_name', data_value)'.
	
	# Uncommment the lines below to enable the other channel feeds.
	
	#aio.send('ads1015_data_ch1', ch1)
	#aio.send('ads1015_data_ch2', ch2)
	#aio.send('ads1015_data_ch3', ch3)
	
	time.sleep(1) #Sleep before taking another reading. Value is in seconds, 60=1min, 3600=1hour.
