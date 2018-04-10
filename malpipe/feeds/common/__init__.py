#!/usr/bin/env python
#Description     : Common objects for feed modules.
#Author          : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date            : 2017 12 27
#==============================================================================

import os
import sys
sys.path.extend(["../../../"])


from malpipe.feeds.common.local_types import File, URL, Domain, IPAddress
import malpipe.exporters.common 
import malpipe.processors.common

import re
import copy

class MalwareFeedDescription(object):
    def __init__(self, module_name, interval, description, authors, version ):
        self.module_name = module_name
        self.interval = interval
        self.description = description
        self.authors = authors
        self.version = version

    def __str__(self):
        return "%s (%s) - %s" % (self.module_name, self.version, self.description)

class MalwareFeedResults(object):
    def __init__(self, feedmeta):
        self.metadata = feedmeta

        self.files = []
        self.urls = []
        self.domains = []
        self.ipaddresses = []

        self.REGEX_IP = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
        self.REGEX_DNS = "^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$"

    def add_file(self, fData, metadata = {}):
        self.files.append( copy.deepcopy(File( self.metadata.module_name, fData, metadata) ))

    def add_url(self, turl, metadata = {}):
        furl = copy.deepcopy(URL( self.metadata.module_name, turl, metadata))
        self.urls.append( furl )
        if "host" in furl.metadata.keys():
            if re.match(self.REGEX_IP, furl.metadata['host']):
                self.add_ipaddress( furl.metadata['host'], {'url': turl} )
            elif re.match(self.REGEX_DNS, furl.metadata['host']):
                self.add_domain( furl.metadata['host'], {'url': turl} )


    def add_domain(self, tDomain, metadata = {}):
        if re.match(self.REGEX_DNS, tDomain):
            fDamain = copy.deepcopy(Domain( self.metadata.module_name, tDomain, metadata))
            self.domains.append( fDamain )
            return True
        return False
        
    def add_ipaddress(self, tIPAddress, metadata = {}):
        if re.match(self.REGEX_IP, tIPAddress):
            fIP = copy.deepcopy(IPAddress( self.metadata.module_name, tIPAddress, metadata))
            self.ipaddresses.append( fIP )
            return True
        return False

    def get(self):
        return { 
            'files'       : self.files,
            'urls'        : self.urls,
            'domains'     : self.domains,
            'ipaddresses' : self.ipaddresses,
        }
        
    def clear_temp_files(self):
        for f in self.files:
            f.delete_temp()


class MalwareFeed(object):
    def __init__(self,metadata):
        self.metadata = metadata
        self.results = MalwareFeedResults(self.metadata)

        self.processors = []
        self.exporters = []

    def get_metadata(self):
        return self.metadata

    def get_module_name(self):
        return self.metadata.module_name

    def export(self):
        print "[%s] Running Exporters" % ( self.get_module_name())        
        tResults = self.results.get()
        for lExporter in malpipe.exporters.common.Modules.Exporters:
            if lExporter.metadata.module_name in self.exporters:
                for res in tResults.keys():
                    if res in lExporter.types:
                        if len(tResults[res]) > 0:                    
                            lExporter.run( self, res, tResults[res] )
        self.clear_results()

    def clear_results(self):
        self.results.clear_temp_files()
        del(self.results)
        self.results = MalwareFeedResults(self.metadata)

    def process(self):
        print "[%s] Running Processors" % ( self.get_module_name())
        tResults = self.results.get()
        for lProcessor in malpipe.processors.common.Modules.Processors:
            if lProcessor.metadata.module_name in self.processors:
                for res in tResults.keys():
                    if res in lProcessor.types:
                        if len(tResults[res]) > 0:
                            lProcessor.run( self, res, tResults[res] )
class Modules:
    Feeds = []

