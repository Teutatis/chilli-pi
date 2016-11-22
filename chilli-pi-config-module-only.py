#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  chilli-pi.cfg
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
#  
######################

[io]
# Your Adafruit IO key here:
# key=xxx

[sensors] # GPIO pin allocation
# digital_moisture_sensor_pin=17
# name2_pin=18

[parameters] # Setpoints for temperature colour changes etc. to go here.
# soil_temp_yellow_setpoint = 15
# soil_temp_red_setpoint = 10

[email] # SMTP email details, password, login, etc.
# smtp_username = "enter_username_here" # This is the username used to login to your SMTP provider
# smtp_password = "enter_password_here" # This is the password used to login to your SMTP provider
# smtp_host = "enter_host_here" # This is the host of the SMTP provider
# smtp_port = 25 # This is the port that your SMTP provider uses

# smtp_sender = "sender@email.com" # This is the FROM email address
# smtp_receivers = ['receiver@email.com'] # This is the TO email address
