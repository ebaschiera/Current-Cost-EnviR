Current Cost EnviR reader tool
==============================

This is a simple command line tool for fetching the current energy usage and temperature from a Current Cost EnviR electricity usage meter. Data will be stored into two files, /tmp/__currentcost_temp and /tmp/__currentcost_watt. Those files can be read by other scripts to gather data. For immediate data elaboration, the '-a' option will invoke a custom shell script after a successful read from EnviR.

It has been tested against the EnviR meter, but may well work with other meters in the current cost range.
	
Usage:
------
	
	python current-cost.py [-a shell-script-to-run]

Where:

 * shell-script-to-run: is an optional shell script to run after a successful read of watt and temperature from EnviR (for example a script to log new data)

The script reads temperature and energy usage from sensor 0.

The temperature value is written into /tmp/__currentcost_temp

The energy usage value is written into /tmp/__currentcost_watt

Data is written in numeric form, without measure unit.

Limitations:
------------

 * This has been tested against the EnviR, but may well work with other devices in the range (if you change the baud rate).
 * Currently this only supports one sensor connected to the device.
 * If you run this script via cron, don't expect to get new data at every run, because EnviR sometimes outputs a summary message instead of the current data. In that case the script doesn't write new data into files.

Requirements:
-------------
 
 * Python 2
 * pySerial

See
===

 * Marcus Povey <http://www.marcus-povey.co.uk>
 * Current Cost <http://www.currentcost.com/>
	 
