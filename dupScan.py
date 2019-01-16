import os
import hashlib
import shutil
import click
import config

class ScanJob(object):
    '''class for the scan job'''
    duplicates = []
    HashTable = set()

    duplicatesPath = None
    hashFuc = None
    noLog = False
    scanDir:str = None
    moveFlag = None
    dumpFile= None
    configData = config.configfile()
    
    def __init__(self,hashFuc:str,noLog:bool,scanDir:str, configData:config.configfile, moveFlag:bool=False, cMove:str=None):
        self.hashFuc = hashFuc
        self.noLog = noLog
        self.scanDir = scanDir
        self.configData = configData
        self.moveFlag = moveFlag
        self.duplicatesPath = cMove if cMove != None else self.configData.dupDir

    def start(self):
        if not self.noLog:
            self.openDumpFile()

        self.ScanDir()
        if self.moveFlag:
            self.moveDuplicates()
        else:
            self.printDuplicates()

    def ScanDir(self, path=None):
        '''Scan the  directory'''
        scanPath = path if path != None else self.scanDir
        with os.scandir(scanPath) as diry:
            s = list(diry)
            for entry in s:
                if entry.is_dir():
                    self.logLine(entry.path)
                    self.ScanDir(entry.path)
                else:
                    filename = entry.path
                    File = open(filename, "rb")
                    fileHash = self.getHash(File)
                    if fileHash in self.HashTable: # check if the hash of the file is in the HashTable
                        self.duplicates.append(entry)
                    else:
                        self.HashTable.add(fileHash)
                    self.logLine(f'{entry.stat().st_size}')
                if entry == s[-1]:
                    self.logLine(f'<–––––––––––––––––––––––>')

    def printDuplicates(self):
        for entry in self.duplicates:
                self.logLine(f'{entry.name} from {entry.path} is a duplicate')
        self.logLine(f'Total number of duplicates : {len(self.duplicates)}')


    def moveDuplicates(self):
        self.logLine(f'Total number of duplicates : {len(self.duplicates)}')
        with click.progressbar(self.duplicates,length=len(self.duplicates), label='Moving duplicates') as duplicates:
            for entry in duplicates:
                self.logLine(f'{entry.name} from {entry.path} is a duplicate')
                shutil.move(entry.path, f'{self.duplicatesPath}/{entry.name}')
                self.logLine(f'Moved {entry.name} from {entry.path} to {self.duplicatesPath}/{entry.name}')
    
    def logLine(self, messageOut: str):
        '''Log <messageOut> '''
        click.echo(messageOut) # print to termnal/console
        if not self.noLog:
            self.dumpFile.write(f'{messageOut}\n') # output to dumpfile

    def openDumpFile(self):
        '''Open dumpFile'''
        pathName = self.scanDir.replace('/', '-').replace('.', '')
        dumpFilePath = self.configData.dumpDir
        dumpFile = open(f'{dumpFilePath}/{pathName}.txt', 'w')
        self.dumpFile = dumpFile
    
    def getHash(self, File):
        '''Get the hash of <File>'''
        if self.hashFuc == 'sha256':
            m = hashlib.sha256()
        elif self.hashFuc == 'sha1':
            m = hashlib.sha1()
        elif self.hashFuc == 'sha512':
            m = hashlib.sha512()
        else:
            m = hashlib.md5()            

        m.update(bytearray(File.read()))
        hash = m.hexdigest()
        return hash