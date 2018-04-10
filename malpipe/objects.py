#!/usr/bin/env python
#Description     : Initialization for malpipe modules
#Author          : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date            : 2017 12 27
#==============================================================================

import time
import threading
import feeds 
import exporters
import processors


# FeedRunner creates a thread for each feed for parsing.
# Input: Feed() object
class FeedRunner(threading.Thread):
    def __init__(self, _feedObject):
        super(FeedRunner, self).__init__()
        self.feed = _feedObject
        self.meta = _feedObject.metadata
        self.active = False

    def getInterval(self):
        return self.meta.interval

    def run(self):
        time.sleep(0.5)
        print '[R] Running %s' % self.meta.module_name
        try:
            self.active = True        
            self.feed.run()
        except Exception, e:
            print "[%s] Module error (%s).  Restarting." % (self.feed.get_module_name(), e)
            self.active = False
        print "[%s] Finished" % self.feed.get_module_name()

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





