import os
import hashlib
import shutil
import click

duplicates = []
HashTable = set()



def scanDir(path):
    with os.scandir(path) as diry:
        test = list(diry)
        for entry in test:
            if entry.is_dir():
                print(entry.path)
                scanDir(entry.path)
            else:
                filename = entry.path
                # print(filename)
                File = open(filename, "rb")
                fileHash = getHash(File)
                if fileHash in HashTable: # check if the hash of the file is in the HashTable
                    duplicates.append(entry)
                HashTable.add(fileHash)
                scanDump.write(f'{entry.name} | {entry.is_dir()}\n')
                print(f'    {entry.name} | {entry.is_dir()}')
            if entry == test[-1]:
                scanDump.write('<------------------------------> \n')
                print('<------------------------------>')
    
def getHash(File):
    m = hashlib.md5()
    m.update(bytearray(File.read()))
    hash = m.hexdigest()
    return hash

def openDumpFile(pathName: str, dumpFilePath:str):
    pathName = pathName.replace('/','-').replace('.','')
    dumpFile = open(f'{dumpFilePath}/{pathName}.txt', 'w')
    return dumpFile
    

def printDuplicates(duplicates:list):
    for entry in duplicates:
        print(f'{entry.name} from {entry.path} is a duplicate')
        scanDump.write(f'{entry.name} from {entry.path} is a duplicate\n')      
    print(f'Total number of duplicates : {len(duplicates)}\n')
    scanDump.write(f'Total number of duplicates : {len(duplicates)}\n')
    moveDuplicates(duplicates)

def moveDuplicates(duplicates: list):
    duplicatesPath = 'ScanDump/duplicates'
    for entry in duplicates:
        shutil.move(entry.path, f'{duplicatesPath}/{entry.name}')
        print(f'Moved {entry.name} from {entry.path} to {duplicatesPath}/{entry.name}')
        scanDump.write(f'Moved {entry.name} from {entry.path} to {duplicatesPath}/{entry.name}\n')

def logLine(noLogFlag:bool, messageOut:str):
    click.echo(messageOut)
    if not noLogFlag:
        # output to dumpfile
        pass

#  print('Enter a Path for be scaned:')
# path = input()
# scanDump = openDumpFile(path)
# scanDump.write(f'{path}\n')
# scanDir(path)
# printDuplicates(duplicates)
# scanDump.close() 