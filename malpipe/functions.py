#!/usr/bin/env python
#Description     : Core / Shared functions used by Malpipe
#Author          : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date            : 2017 12 27
#==============================================================================

import schedule
import time
import objects

# Starts daemon feeds and schedules ones to run at 
# later times
def SetupFeeds(feedList):
	for name, handle in feedList:
		interval = handle.getInterval()
		if interval == None and handle.active == False:
				handle.setDaemon(True)
				handle.start()
		else:
			try:
				interval.do( handle.start )
			except Exception,e:
				print "[X] Problem starting %s feed: %s" % ( name, e)

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

	SetupFeeds( feeds )

	while True:
		schedule.run_pending()
		time.sleep(10)


