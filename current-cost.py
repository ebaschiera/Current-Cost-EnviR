#!/usr/bin/python
###
# current-cost.py
#
# This is a simple tool for reading the latest values from a current cost energy
# meter. This works with my Current Cost EnviR, but it might work with other
# meters in the range.
# This tool will write /tmp/__currentcost_[sensor_id]_watt files, where sensor_id 
# is taken from the target_sensors list.
# Output is raw numbers.
# Put this in the system cron, to be executed every minute.
# You can call this script with an argument, that is a shell script to be run if
# the reading is successful. That shell script can be a data logger command, for
# example.
# To execute a script after reading, use:
# python current-cost.py [-a|--after-read-run shell_script_name]
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

import getopt
import sys
import serial
import re
import os
import pprint

def main():
	
	port = '/dev/envir'
	baud = 57600
	timeout = 10
	retry = 3
	target_sensors = ["0", "1"]
	after_read_run_script = None
	read_data = {}


	try:
		opts, args = getopt.getopt(sys.argv[1:], "a", ["after-read-run"])
	except getopt.GetoptError, err:
		print str(err)
		sys.exit()

	for o, a in opts:
		if o in ("-a", "--after-read-run"):
			after_read_run_script = args[0]
	
	meter = serial.Serial(port, baud, timeout=timeout)
	if meter.isOpen() == False:
		meter.open()

	# init read_data which will contain resulting reads
	for target_sensor in target_sensors:
		read_data[target_sensor] = False

	# pprint.pprint(read_data)

	for target_sensor in target_sensors:
		if read_data[target_sensor] != False:
			continue

		current_iteration_retry = retry
		data = False
		
		while (not data) or (current_iteration_retry > 0):
			current_iteration_retry = current_iteration_retry - 1
			try:
				data = meter.readline()
				if (data):
					sensor_value = readSensorData(data)
					if (read_data != False):
						read_data.update(sensor_value)
			except:
				continue

	# pprint.pprint(read_data)
	
	meter.close()

	writeDataToDisk(read_data)
	
	# invoke datalogger trigger
	if after_read_run_script != None:
		if os.path.isfile(after_read_run_script):
			os.system('sh ' + after_read_run_script)

def readSensorData(data_line):
	#pprint.pprint(data_line)
	try:
		sensor_ex = re.compile('<sensor>([0-9])</sensor>')
		sensor_id = sensor_ex.findall(data_line)[0]
	except:
		# sys.stderr.write("Could not get a sensor id from device\n")
		return False
	try:
		watts_ex = re.compile('<watts>([0-9]+)</watts>')
		watts = str(int(watts_ex.findall(data_line)[0])) # cast to and from int to strip leading zeros
	except:
		# sys.stderr.write("Could not get a watt value from device")
		return False
	parsed_data = {sensor_id: watts}
	return parsed_data

def writeDataToDisk(read_data):
	if not os.path.isfile('/tmp/__currentcost_2.lock'):
		os.system('touch /tmp/__currentcost_2.lock')
		for (sensor_id, watt_value) in read_data.items():
			if (watt_value):
				# sys.stdout.write("Found value " + watt_value + " for sensor " + sensor_id + "\n")
				os.system('echo "' + watt_value + '" > /tmp/__currentcost_"' + sensor_id + '"_watt.tmp 2> /tmp/__currentcost_"' + sensor_id + '"_watt.err && mv /tmp/__currentcost_"' + sensor_id + '"_watt.tmp /tmp/__currentcost_"' + sensor_id + '"_watt& ')
			else:
				# sys.stdout.write("Not found values for sensor " + sensor_id + "\n")
		os.system('rm /tmp/__currentcost_2.lock')
	else:
		os.system('rm /tmp/__currentcost_2.lock')

if __name__ == "__main__":
    main()
