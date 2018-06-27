#!/usr/bin/env python
#Description	 : Initialization for malpipe modules
#Author		  : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date			: 2017 12 27
#==============================================================================

import time
import threading
import schedule
import feeds 
import exporters
import processors



# Threat Status flags
class threatStatus:
	ready = 0
	start = 1
	running = 2
	error = 3
	finished = 4

# FeedRunner creates a thread for each feed for parsing.
# Input: Feed() object
class FeedRunner(threading.Thread):
	def __init__(self, _feedObject):
		super(FeedRunner, self).__init__()
		self.feed = _feedObject
		self.meta = _feedObject.metadata
		self.status = threatStatus.ready

		interval = self.getInterval()
		if interval is None:
			self.setDaemon(True)
		else:
			interval.do( self.signal_start )

	#Used for scheduled threads
	def signal_start(self):
		self.status = threatStatus.start

	def getInterval(self):
		return self.meta.interval

	def getName(self):
		return self.feed.get_module_name()

	def run(self):
		time.sleep(0.5)
		print "Starting %s" % self.feed.get_module_name()
		try:
			while True:
				if self.getInterval() is None:
					self.status = threatStatus.running		
					self.feed.run()
					self.status = threatStatus.finished	

				else:
					if self.status == threatStatus.start:
						self.status = threatStatus.running	
						self.feed.run()
						self.status = threatStatus.ready	

#					else:
#						print "%s waiting...%s" % (self.getName(), self.status)

					time.sleep(30)
		except Exception, e:
			print "[%s] Module error (%s).  Restarting." % (self.getName(), e)
			self.status = threatStatus.error

		print "[%s] Thread Exited" % self.getName()


class Feeds(object):
	def __init__(self):
		self._feeds = {}
		for m in feeds.common.Modules.Feeds:
			runner = FeedRunner(m)
			self._feeds[m.metadata.module_name] = runner

	def __iter__(self):
		for elem in self._feeds.keys():
			yield (elem, self._feeds[elem])

	def __getitem__(self, item):
		yield( self, self._feeds[item] )

	def print_list(self):
		print "[Feeds] %s" % ( ", ".join(self._feeds.keys()) )

	def start(self):
		for name in enumerate(self._feeds):
			tFeed = self._feeds[name[1]]
			tFeed.start()

class Processors(object):
	def __init__(self):
		self._feeds = {}
		for m in processors.common.Modules.Processors:
			self._feeds[m.metadata.module_name] = None
			
	def __iter__(self):
		for elem in self._feeds.keys():
			yield (elem, self._feeds[elem])

	def __getitem__(self, item):
		yield( self, self._feeds[item] )

	def print_list(self):
		print "[Processors] %s" % ( ", ".join(self._feeds.keys()) )

			
class Exporters(object):
	def __init__(self):
		self._feeds = {}
		for m in exporters.common.Modules.Exporters:
			self._feeds[m.metadata.module_name] = None
			
	def __iter__(self):
		for elem in self._feeds.keys():
			yield (elem, self._feeds[elem])

	def __getitem__(self, item):
		yield( self, self._feeds[item] )

	def print_list(self):
		print "[Exporters] %s" % ( ", ".join(self._feeds.keys()) )




