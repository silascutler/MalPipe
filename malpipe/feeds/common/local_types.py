#!/usr/bin/env python
#Description     : Common types for feed modules.
#Author         : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date         : 2018 04 04 
#==============================================================================

import os
import hashlib
from urlparse import urlparse

class Indicator(object):
    def __init__(self, source, itype, indata, metadata = {}  ):
        self.type = itype
        self.value = indata
        self.source = source 
        self.metadata = metadata
        self.tmp_path = None

    def __str__(self):
        return "[%s] %s (%s)" % (self.type, self.value, self.source)



class URL( Indicator, object ):
    def __init__(self, source, indata, metadata = {} ):
        Indicator.__init__(self, source, "url", indata, metadata)
        self.parse(indata)

    def parse(self, inurl):
    	try:
        	o = urlparse(inurl)
        	self.metadata['host'] = o.hostname
        	self.metadata['path'] = o.path
        except Exception,e:
        	pass

class Domain( Indicator ):
    def __init__(self, source, indata, metadata = {} ):
        Indicator.__init__(self, source, "domain", indata, metadata)
        

class IPAddress( Indicator ):
    def __init__(self, source, indata, metadata = {} ):
        Indicator.__init__(self, source, "ipaddress", indata, metadata)
        

class File( Indicator ):
    def __init__(self, source, indata, metadata = {} ): 
        Indicator.__init__(self, source, "file", indata, metadata)
        if "hashes" not in self.metadata.keys(): 
            self.metadata['hashes'] = self.hashFile(indata)
            self.save_temp()

    def hashFile(self, indata):
        hashes = {
            'md5' : hashlib.md5( indata ).hexdigest(),
            'sha1' : hashlib.sha1( indata ).hexdigest(),
            'sha256' : hashlib.sha256( indata ).hexdigest(),
        }
        return hashes

    def save_temp(self):
        tmp_path = "./.tmp_downloads/" + self.source + "/"
        if not os.path.exists(tmp_path):
                os.makedirs(tmp_path)
        self.tmp_path = tmp_path + self.metadata['hashes']['sha256']

        fhandle = open(self.tmp_path, "wb")
        fhandle.write(self.value)
        fhandle.close()
        self.value = self.metadata['hashes']['sha256']

    def delete_temp(self):
        if self.tmp_path == None:
            return True
        try:
            if os.path.isfile(self.tmp_path):
                os.remove(self.tmp_path)
        except Exception, e:
            pass

    def __str__(self):
        return "[%s] %s - %s" % (self.type, self.source, self.tmp_path)


        














