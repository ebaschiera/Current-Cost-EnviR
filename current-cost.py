#!/usr/bin/python
###
# current-cost.py
#
# This is a simple tool for reading the latest values from a current cost energy
# meter. This works with my Current Cost EnviR, but it might work with other
# meters in the range.
# This tool will write /tmp/__currentcost_watt and /tmp/__currentcost_temp from 
# sensor 0.
# Output is raw numbers.
# Put this in the system cron, to be executed every minute.
# 
# @author Marcus Povey <marcus@marcus-povey.co.uk>
# @copyright Marcus Povey 2013
# @contributor Ermanno Baschiera <ebaschiera@gmail.com>
# @link http://www.marcus-povey.co.uk
# 
# Copyright (c) 2013 Marcus Povey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###

import sys
import serial
import re
import os

def main():
	
	port = '/dev/ttyUSB0'
	baud = 57600
	timeout = 10
	retry = 3
	target_sensor = "0"
	
	meter = serial.Serial(port, baud, timeout=timeout)
	if meter.isOpen() == False:
		meter.open()
	
	try:
		data = meter.readline()
	except:
		pass
	while (not data) and (retry > 0):
		retry = retry - 1
		try:
			data = meter.readline()
		except:
			pass
	
	meter.close()

	try:
		sensor_ex = re.compile('<sensor>([0-9])</sensor>')
		sensor = sensor_ex.findall(data)[0]
		if sensor != target_sensor:
			#sys.stderr.write("Not the right sensor")
			sys.exit()
		
	except:
		#sys.stderr.write("Could not get details from device")
		sys.exit()
	
	try:
		watts_ex = re.compile('<watts>([0-9]+)</watts>')
		temp_ex = re.compile('<tmpr>([\ ]?[0-9\.]+)</tmpr>') # when temperature is less than 10, currentcost adds a space before the number
		time_ex = re.compile('<time>([0-9\.\:]+)</time>')
		
		watts = str(int(watts_ex.findall(data)[0])) # cast to and from int to strip leading zeros
		temp = temp_ex.findall(data)[0].strip() # remove that extra space
		time = time_ex.findall(data)[0]
	except:
		#sys.stderr.write("Could not get details from device")
		sys.exit()

	if not os.path.isfile('/tmp/__currentcost.lock'):
		os.system('touch /tmp/__currentcost.lock && echo "' + watts + '" > /tmp/__currentcost_watt.tmp 2> /tmp/__currentcost_watt.err && mv /tmp/__currentcost_watt.tmp /tmp/__currentcost_watt && echo "' + temp + '" > /tmp/__currentcost_temp.tmp 2> /tmp/__currentcost_temp.err && mv /tmp/__currentcost_temp.tmp /tmp/__currentcost_temp && rm /tmp/__currentcost.lock & ')
	else:
		os.system('rm /tmp/__currentcost.lock')
	
if __name__ == "__main__":
    main()
