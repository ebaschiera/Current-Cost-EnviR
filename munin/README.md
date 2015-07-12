Current Cost Munin plugin
==========================
	
This directory contains a plugin for munin <http://munin-monitoring.org/> to monitor the output of a Current Cost EnviR meter. You can monitor several sensors. Only temperature and energy usage are supported.

This plugin reads data from the following files:

 * /tmp/\_\_currentcost\_watt\_[sensor\_id] for the energy usage
 * /tmp/\_\_currentcost\_temp\_[sensor\_id] for the temperature
 
Replace [sensor\_id] with the sensor number you want to monitor.

Usage:
------

 * Install the files from this repo somewhere sensible
 * Link to the file from /etc/munin/plugins as normal (the following example uses sensor number 1)
	* cd /etc/munin/plugins
	* ln -s /path/to/plugins/currentcost\_ currentcost\_watts\_1
	* ln -s /path/to/plugins/currentcost\_ currentcost\_temp\_1

 * Restart munin-node


See
---

 * Marcus Povey <http://www.marcus-povey.co.uk>
 * Current Cost <http://www.currentcost.com/>
	 
