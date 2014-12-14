Current Cost Munin plugin
==========================
	
This directory contains a plugin for munin <http://munin-monitoring.org/> to monitor the output of a Current Cost EnviR meter. Only temperature and energy usage are supported.

This plugin reads data from the following files:

 * /tmp/__currentcost_watt for the energy usage
 * /tmp/__currentcost_temp for the temperature

Usage:
------

 * Install the files from this repo somewhere sensible
 * Link to the file from /etc/munin/plugins as normal
	cd /etc/munin/plugins
	ln -s /path/to/plugins/currentcost_ currentcost_watts
	ln -s /path/to/plugins/currentcost_ currentcost_temp

 * Restart munin-node


See
---

 * Marcus Povey <http://www.marcus-povey.co.uk>
 * Current Cost <http://www.currentcost.com/>
	 
