#!/usr/bin/env python
#Description     : Common objects for Processors. 
#Author          : Silas Cutler (Silas.Cutler@BlackListThisDomain.com)
#Date            : 2017 12 27
#==============================================================================

class ProcessorDescription(object):
    def __init__(self, module_name, description, authors, version ):
        self.module_name= module_name 
        self.description = description
        self.authors = authors
        self.version = version

    def __str__(self):
        return "%s (%s) - %s" % (self.module_name, self.version, self.description)

class Processor(object):
    def __init__(self,metadata):
        self.metadata = metadata
        self.types = []

    def get_metadata(self):
        return self.metadata

    def get_module_name(self):
        return self.metadata.module_name

class Modules:
    Processors = []

