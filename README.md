Current Cost EnviR reader tool
==============================

This is a simple command line tool for fetching the current energy usage and temperature from a Current Cost EnviR electricity usage meter. Data will be stored into multiple files in pairs, /tmp/\_\_currentcost\_[sensor\_id]\_temp and /tmp/\_\_currentcost\_[sensor\_id]\_watt. The [sensor_id] value depends on the installed sensors. Those files can be read by other scripts to gather data. For immediate data elaboration, the '-a' option will invoke a custom shell script after a successful read from EnviR.

It has been tested against the EnviR meter, but may well work with other meters in the current cost range.
	
Usage:
------
	
	python current-cost.py [-a shell-script-to-run]

Where:

 * shell-script-to-run: is an optional shell script to run after a successful read of watt and temperature from EnviR (for example a script to log new data)

The script reads temperature and energy usage from sensors specified in the variable "target_sensors".

The temperature value is written into /tmp/\_\_currentcost\_[sensor\_id]\_temp

The energy usage value is written into /tmp/\_\_currentcost\_[sensor\_id]\_watt

Data is written in numeric form, without measure unit.

Limitations:
------------

 * This has been tested against the EnviR, but may well work with other devices in the range (if you change the baud rate).
 * If you run this script via cron, you should get new data at every run, even if EnviR sometimes outputs a summary message instead of the energy data. If the script can't get any data, no files will be written.

Requirements:
-------------
 
 * Python 2
 * pySerial

See
===

 * Marcus Povey <http://www.marcus-povey.co.uk>
 * Current Cost <http://www.currentcost.com/>
	 
