# This is template assignment 2
import sys,os
# sys supports the commandline arguments.
import sqlite3
# sqlite3 is used to establish a database for query

# Start of program logic: check wether a local db is present at the current folder
#for item in sys.argv:
#    print item

# get current directory path
cwd = os.getcwd()
# Running the script alone is not supported.
if (len(sys.argv) == 1):
    print "Running this script with no argument is not supported!"
elif (len(sys.argv)==2):
    if (sys.argv[1] == "cwd"):
        print "your are executing", os.path.abspath(sys.argv[0]), "in", cwd
# Command type 1: argc = 2
# this.py info, status
    elif (sys.argv[1] == "info"):
        print "This is an SCM script for CSC444 assignment 2"
        print "The solution is provided by Ximeng Wang and Wenzhong Zhang"
    elif (sys.argv[1] == "status"):
        try:
            with open('myDB.db'):
                print "The directory is under SCM."
        except IOError:
            print 'The directory is not under SCM. Use add command to start'
    elif (sys.argv[1] == "list"):
        # get an array of filenames in files.
        files = os.listdir(cwd)
        print "The directory contains the following files:"
        for file in files:
            print " -",file
# Command type 2: argc = 3
# this.py 
elif (len(sys.argv) >= 3):
    print "3 or more arg's: Currently under development. Why not coming back later??"


# Database object. Pending. 
def myDB(object):
    pass

