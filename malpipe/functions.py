#!/usr/bin/env python
#Description	 : Core / Shared functions used by Malpipe
#Author		  : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date			: 2017 12 27
#==============================================================================

import schedule
import time
import objects

# Starts daemon feeds and schedules ones to run at 
# later times

#Main program runner
def run():
	# Load all modules and print active list
	feeds = objects.Feeds()
	exporters = objects.Exporters()
	processors = objects.Processors()
	print "Active Modules:"
	feeds.print_list()
	processors.print_list()	
	exporters.print_list()

	print "\nStarting..."

	feeds.start()

	while True:
		try:
			schedule.run_pending()
		except Exception, e:
			print "Excepion running pending: %s" % (e)
		time.sleep(10)


