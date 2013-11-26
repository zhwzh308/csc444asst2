# This is template assignment 2
import sys, os, getopt
# sys supports the commandline arguments.
import sqlite3
# sqlite3 is used to establish a database for query

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def databaseVerifier(filename):
    try:
        with open(filename):
            return True
    except IOError:
        return False

# get current directory path
def main(argv=None):
    if argv is None:
        argv = sys.argv
        # etc. replacing sys.argv with argv  in the getopt call.
    cwd = os.getcwd()
    print len(argv), "arguments supplied."
    try:
        try:
            opts, args = getopt.getopt(argv[1:],"h",["help"])
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2
    # Error checking complete
    if (len(argv) == 1):
        print "Running this script with no argument is not supported!"
        print "In order to work with this SCM, you need to use command such as"
        print " - cwd : current working dir"
        print " - info : about this program"
        print " - status : system status of this directory"
        print " - list : list all files under this directory(non-recursively)"
    elif (len(argv)==2):
        if (argv[1] == "cwd"):
            print "your are executing", os.path.abspath(argv[0]), "in", cwd
        elif (argv[1] == "info"):
            print "This is an SCM script for CSC444 assignment 2"
            print "The solution is provided by Ximeng Wang and Wenzhong Zhang"
        elif (argv[1] == "status"):
            if (databaseVerifier('myDB.db')):
                print "The directory is under SCM."
            else:
                print 'The directory is not under SCM. Use add command to start'
        elif (argv[1] == "list"):
            # get an array of filenames in files.
            files = os.listdir(cwd)
            print "The directory contains the following files:"
            for file in files:
                print " -",file
        elif (argv[1] == "add" or argv[1] == "del"):
            print "Add/del: need more arguments"
        else:
            print argv[1], "(command not reconized)"
            # Command type 2: argc = 3
            # this.py
    elif (len(argv) == 3):
        print "3 or more arg's: Currently under development."
        if (argv[1] == "add"):
            if(databaseVerifier('myDB.db')):
                print "Adding file",argv[2],"to the SCM database"
            else:
                print "Creating database."
                if (databaseVerifier('myDB.db')):
                    print "Opearation succeeded. Adding file into the database."
                else:
                    print 'Database creation failed. Check if you have right to the directory', cwd
        elif (argv[1] == "del"):
            print "delete file",argv[2],"from database"
        else:
            print argv[1],"is not supported."
    else: # We know there are more args. keep print them.
        if (argv[1]=='add'):
            print "adding "
        elif (argv[2]=='del'):
            print "deleting "
        else:
            print "not supported"

# End of main
if __name__ == "__main__":
    sys.exit(main())

def myDB(object):
    pass

