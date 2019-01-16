# imports
import os
import click
import jsonpickle
import config as con
import dupScan

config = con.configfile()

@click.group()
@click.option('-f', '--file', 'filepath', help='run with a temp config')
def cli(filepath=None):
    '''
    DataDeDup is a CLI tool to help find duplicates of files in a large directory\n

    Run `DataDeDup setup` to setup the config
    '''
    global config
    # check if a temp config file has been parsed
    localconfig = filepath if filepath != None else './config.json'
    
    # Check for local config
    exists = os.path.isfile(localconfig)
    if exists:
        config = con.configfile(path=localconfig)
        click.echo(f'Config: {config.path},    \nDumpFile directory: {config.dumpDir}\nduplicates directory: {config.dupDir}')
        pass
    else:
        setup()
        pass
        

@click.command('scan', short_help='Performs a scan of duplicate in specified directory')
@click.option('-m', '--move', help='Move duplicates to the duplicates directory', is_flag=True)
@click.option('-c', '--custom-move','cmove', help='Move duplicates to custom duplicates directory',type=str)
@click.option('-h', '--hash','hashfuc', help='Pick your preferred hash type', type=click.Choice(['md5', 'sha1']),show_default=True, default='md5')
@click.option('--no-log','log', help='Disable logging of the scan output to dumpfile', is_flag=True)
@click.argument('path')
def scan(move,cmove, hashfuc, log, path):
    '''Performs a scan of duplicate in specified directory'''
    global config 
    click.echo(f'move flag: {move}\n custom-move: {cmove}\n hash Choice: {hashfuc}\n no log: {log}\n dir path: {path}')  # debug print
    newJob = dupScan.ScanJob(hashfuc, log, path, config, move, cmove)
    newJob.start()

@click.command('setconfig',short_help='Change config file')
@click.option('-f', '--file', 'Filepath',help='import existing DataDeDup config file', type=str)
def setconfig(Filepath):
    global config 
    # Change config
    if Filepath != None:
        config.importConfig(Filepath)
        click.echo(f'Config: {Filepath},    \nDumpFile directory: {config.dumpDir}\nduplicates directory: {config.dupDir}')
    else:
        pass
    

@click.command('setup',short_help='setup DataDeDup')
def setup():
    # setup config file
    global config 
    click.echo('DataDeDup initial setup')
    if click.confirm('Do you want to import a existing DataDeDup config file?'):
        Filepath = click.prompt('Please enter path to config file', type=str)
        config.importConfig(Filepath)
        click.echo(f'Config: {Filepath},    \nDumpFile directory: {config.dumpDir}\nduplicates directory: {config.dupDir}')
    else:
        dumpDir = click.prompt('Enter a path for the DumpFile directory', type=str)
        dupDir = click.prompt('Enter a path for the duplicates directory', type=str)
        config = con.configfile(dumpDir, dupDir)
        click.echo(f'Config: {config.path},    \nDumpFile directory: {config.dumpDir}\nduplicates directory: {config.dupDir}')


cli.add_command(scan)
cli.add_command(setconfig)
cli.add_command(setup)
