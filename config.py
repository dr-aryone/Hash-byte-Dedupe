'''
a module for the configfile class
'''

import jsonpickle
import os

class configfile(object):
    '''Class for the Configfile'''
    dumpDir = ''
    dupDir = ''
    path = ''

    def __init__(self, dumpdir:str=None, dupdir:str=None, path:str=None):
        self.path = path if path != None else './config.json'
        if dumpdir == None and dupdir == None and path != None:
            self.openConfig()
        elif dumpdir != None and dupdir != None:
            self.dupDir = dupdir
            self.dumpDir = dumpdir
            self.saveConfig()
        else:
            pass
        
    def importConfig(self, filePath):
        self.path = filePath
        self.openConfig()
        self.path = './config.json'
        self.saveConfig()

    def openConfig(self):
        configJson = open(self.path, 'r')
        configData = jsonpickle.decode(configJson.read())
        self.dumpDir = configData.dumpDir
        self.dupDir = configData.dupDir

    def saveConfig(self):
        configJson = open(self.path, 'w')
        configJson.write(jsonpickle.encode(self))