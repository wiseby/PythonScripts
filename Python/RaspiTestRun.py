"""
For running test on a raspberry pi and writing the code on anpther machine.
When testing the program om the pi it should update from a remote repository
so the code that has been written on the remote machine gets updated runs.
The program starts the application in a seperate process and capturing any
error.

This Program needs git to run and a remote repository setup with initialized
.git source.

Before testing clone the repository to be tested on the pi. Then run program
from cloned destination.

The program creates a config file where repos and specifik program run
characteristics are declared.

git pull origin master
subprocess.run('program to test')
saves messages to a file as a testlog.

Error 1:
No .git file found.

This should be the part where you have the option to add this and sync to a 
repository of your choosing.

Error 2:
Remote repository not found.
"""
import time
import os
import sys
import subprocess

pythonVersion = 'python3.7'
error = 0
log = []
logFile = 'test.log'
configFile = ''
gitPull = ['git', 'pull', 'origin', 'master']
testProgram = ''
gitHubURL = r'https://github.com/'
logInit = 'Program start {}\n'.format(time.strftime('%D | %H:%M'))


def program():
    """ Main Program."""

    global log
    global error
    global testProgram

    log.append(logInit)

    if len(sys.argv) > 1:
        testProgram = str(sys.argv[1])

    if len(sys.argv) > 2:
        remoteRepo = sys.argv[2]

    testProcess = [pythonVersion, testProgram]

    if (FindFile('.git')):
        git = subprocess.run(
            gitPull,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )
    if (testProgram != ''):
        test = subprocess.run(
            testProcess,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )

        log.append('git stdout\n{0}'.format(git.stdout))
        log.append('\n\r')
        log.append('git stderr\n{0}'.format(git.stderr))
        log.append('\n\r')
        log.append('test stdout:\n{0}'.format(test.stdout))
        log.append('\n\r')
        log.append('test stderr:\n{0}'.format(test.stderr))
        log.append('\n\r')

        WriteToLog(log)

    else:
        error = 1

    sys.exit(error)


def WriteToLog(data):
    """ Writes stdout and stderr to logfile. """
    for line in data:
        with open(logFile, 'a') as f:
            f.write(line)


def FindFile(file):
    DirectoryList = os.listdir()

    for dir in DirectoryList:
        if dir == file:
            return True

if __name__ == '__main__':
    program()
