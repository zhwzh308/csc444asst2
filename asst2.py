# This is template assignment 2
import sys, os, getopt, io, errno
import shutil
# for shell utility
import time
# sys supports the commandline arguments.
import sqlite3
# sqlite3 is used to establish a database for query

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def fileExist(filename):
    try:
        with open(filename):
            return True
    except IOError:
        return False

def addFile(filename):
    srcfolder = os.getcwd()
    srcfile = srcfolder+'/'+filename
    destfolder = srcfolder + '/.scm'
    result = shutil.copy(srcfile, destfolder)

def folderExist(foldername):
    cwd = os.getcwd()
    path = cwd+'/'+foldername
    if os.path.exists(path):
        return os.path.isdir(path)
    else:
        return False

def scmInit(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def fileUnderControl(filename):
    if fileExist(filename) and folderExist('.scm'):
        destfolder = os.getcwd()+'/.scm'
        if fileExist(destfolder+'/'+filename):
            return True
        else:
            return False
    else:
        return False

def helpUserMakeDecision():
    print "CSC444 Software Engineering I: Assignment 2 Source Control Management System"
    print "python asst2.py - print this message"
    print "python asst2.py status - return if any file is under SCM"
    print "python asst2.py status [filename] - find out if [filename] is under SCM"
    print "python asst2.py add [filename] - Source control [filename]"
    print "python asst2.py commit - Commit the file whichever is under SCM"
    print "python asst2.py diff - Diff file which is under SCM"

def processArgs(argc, argv):
    # current working dir.
    scmdir = '.scm'
    if argc == 1:
        helpUserMakeDecision()
    elif argc == 2:
        if argv[0] == 'status':
            if (folderExist(scmdir)):
                print "SCM folder exist."
            else:
                print "No file in this directory is under SCM."
        elif argv[0] == 'add':
            print "Add: need filename"
            helpUserMakeDecision()
        elif (argv[0] == 'init'):
            if folderExist(scmdir):
                print "nothing to be done - this directory has file under SCM."
            else:
                scmInit(scmdir)
                print "Initiate Source Control..."
        elif argv[0] == 'help':
            helpUserMakeDecision()
        else:
            print argv[0], "- command not reconized. Type help for help."
    elif argc >= 3:
        if argv[0] == 'status':
            pass
        elif argv[0] == 'add':
            print 'adding:'
            for item in argv[1:]:
                if fileUnderControl(item):
                    print ' -',item
                else:
                    addFile(item)
                    print ' -',item,'added.'
            print 'done.'
        else:
            print argv[0], 'is not supported.'
    else:
        print 'not supported'
    return 0

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:],"h",["help"])
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2
    return processArgs(len(argv), args)

if __name__ == "__main__":
    sys.exit(main())


