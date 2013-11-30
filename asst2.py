# CSC444 asst2.py
import sys, os, getopt, filecmp, errno
import shutil
# shell utility for file manipulation

# difflib can generate delta. Here we imported two objects.
from difflib import Differ, SequenceMatcher
# a delta is printed by pprint
from pprint import pprint
#Each line of a Differ delta begins with a two-letter code:
#'- '    line unique to sequence 1
#'+ '    line unique to sequence 2
#'  '    line common to both sequences
#'? '    line not present in either input sequence

# To include custom function from another file
#def include(filename):
#    if os.path.exists(filename): 
#        execfile(filename)

# Check if a string is ASCII
def isAscii(line):
	try:
		line.decode('ascii')
	except UnicodeDecodeError:
		# raise
		return False
	else:
		return True
	#finally:
	#	pass
# Check if a file is ASCII
def isAsciiFile(filename):
	f = open(filename, 'r')
	for line in f.readlines():
		if not isAscii(line):
			f.close()
			return False
	f.close()
	return True

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg
# See if a file exist.
def fileExist(filename):
	try:
		with open(filename, 'r'):
			return True
	except IOError:
		return False

def branchExist(branch):
	if folderExist('.scm'):
		if fileExist(os.path.join('.scm',branch)):
			return True
	return False

# UNIX touch, creach an empty file. It is thread safe.
def touch(fname, times=None):
	with file(fname, 'a'):
		os.utime(fname, times)
# Quick check if we comparing the same file.
def isSameFile(nu, old):
	if fileExist(nu) and fileExist(old):
		return filecmp.cmp(nu, old)
	else:
		return False
# Quick check if folder is present in current working directory
def folderExist(foldername):
	if os.path.exists(foldername):
		return os.path.isdir(path)
	else:
		return False

# Determine if current folder has been initialized for SCM
def folderUnderControl():
	if folderExist('.scm'):
		if (fileExist(os.path.join('.scm','main'))):
			return True
		else:
			return False
	else:
		return False

# return a file name string that is the SCM file we currently versioning.
def discoverSCMFile():
	# List of file in cwd
	if folderUnderControl():
		files = os.listdir('.scm')
		cwdfiles = os.listdir(os.path.getcwd())
		for item in files:
			if item in cwdfiles:
				return item
	else:
		return None

# Support Init command
def scmInit(branch='main'):
	scmdir = '.scm'
	branchfile = os.path.join(scmdir,branch)
	try:
		os.makedirs(scmdir)
		touch(branchfile)
		print "Initiate Source Control... done"
	except OSError as exc:
		# Folder exist
		if exc.errno == errno.EEXIST and os.path.isdir(scmdir):
			if (fileExist(branchfile)):
				print 'branch', branch, 'already exist!'
			else:
				touch(branchfile)
				print 'branch', branch, 'created.'
			pass
		else:
			raise

# Add a file to the scm folder
def addFile(filename):
	if fileExist(filename):
		if folderExist('.scm'):
			if fileExist(os.path.join('.scm',filename)):
				print 'File',filename,'was added previously'
				return False
			else:
				shutil.copy(filename, '.scm')
				return True
		else:
			print 'Run init first'
			return False
	else:
		print 'File',filename,'does not exist'
		return False

def getFileName(branch='main', version='0'):
	# find version of the SCM file we currently versioning.
	if folderUnderControl():
		if version != '0':
			version = getLatestVersion(branch)
			if version == '0':
				return False
		for item in os.listdir('.scm'):
			if branch in item:
				if version in item:
					return item
	else:
		print 'error getting latest file from',branch
		return False

def getVersionString(filename):
	return filename.split(str='_')[1]

def getLatestVersion(branch='main'):
	if (folderExist('.scm')):
		filemaster = os.path.join('.scm',branch)
		if fileExist(filemaster):
			f = open(filemaster,'r')
			lines = f.readlines()
			f.close()
			version = ((lines[-1]).split())[0]
			return version
		else:
			print 'branch does not exist'
			return str(0)
	else:
		print 'Directory not initialized'
		return str(0)

def checkoutFile(branch='main', version='0'):
	if version == '0':
		# Check out the newest
		version = getLatestVersion(branch)
		filename = os.path.join('.scm', getFileName(branch,version))
		if fileExist(filename):
			fw = open(discoverSCMFile(),'w')
			fr = open(filename,'r')
			fw.writelines(fr.readlines())
			fw.close()
			fr.close()
		else:
			print 'checkout file failed at',branch,'version',version

def commitFile(branch='main'):
	if folderUnderControl():
		newfile = discoverSCMFile()
		oldfile = '.scm/'+getFileName(branch)
		if isSameFile(newfile, oldfile):
			print 'Nothing to commit.'
		else:
			suffix = '.'+branch+'_'+str(int(getVersionString(getFileName(branch)))+1)
			# suffix for next version file.
			writefile = os.path.join('.scm',newfile)+suffix
			touch(writefile)
			readfile = open(toCommit,'r')
			file1 = open(writefile,'w')
			file1.writelines(readfile.readlines())
			readfile.close()
			file1.close()
			print 'Committed version',version

def comment(comment,branch,version):
	if comment == '':
		print  'on',branch,'- no comment'
	else:
		print 'comment on',branch,'-',comment

# Create diff helper if needed.

def diffFile():
	if folderUnderControl():
		newfile = discoverSCM('.scm')
		oldfile = '.scm/'+newfile
		if isSameFile(newfile, oldfile):
			print "Source file equals to depository file"
		else:
			file1 = open(newfile,'r')
			text1 = file1.readlines()
			file1.close()
			file2 = open(oldfile,'r')
			text2 = file2.readlines()
			file2.close()
			d = Differ()
			result = list(d.compare(text1, text2))
			sys.stdout.writelines(result)
			s = SequenceMatcher(None, text1, text2)
			print 'Your files diff ratio is', s.ratio()

def helpUserMakeDecision():
	print '''
	CSC444 Software Engineering I: Assignment 2 Source Control Management System
	python asst2.py help - print this message
	python asst2.py init - Initiate SCM
	python asst2.py add - return if any file is under SCM
	python asst2.py add [filename] - Source control [filename]
	python asst2.py commit branch [comment] - Commit the change, branch must be specified, and comment are optional.
	python asst2.py checkout - Diff file which is under SCM
	python asst2.py List - Diff file which is under SCM
	python asst2.py branch X- fork a new branch named X based on main
	python asst2.py branch X Y- fork a new branch Y based on X.
	python asst2.py diff - Diff file which is under SCM
	'''

def processArgs(argc, argv):
	# print argc, argv argv starts after python *.py, argv[0] would be the command
	if argc == 0:
		return 2
	else:
		# we judge by command
		command = argv[0]
		if command == 'init':
			if argc == 1:
				scmInit()
			elif argc==2:
				scmInit(argv[1])
			else:
				print 'Bad usage, init, or init branch'
		elif command == 'add':
			if argc == 2:
				pass
			else:
				print 'Bad usage, add filename'
		elif command == 'commit':
			if argc == 1:
				pass
			elif argc == 2:
				pass
			elif argc == 3:
				pass
			else:
				print 'Bad usage, commit [branch] [comment]'
		elif command == 'checkout':
			if argc == 2:
				pass
			elif argc == 3:
				pass
			elif argc == 4:
				pass
			else:
				print 'Bad usage, checkout # or checkout branch #'
		elif command == 'list':
			if argc == 1:
				pass
			elif argc == 2:
				pass
			else:
				print 'Bad usage, list [branch]'
		elif command == 'branch':
			if argc == 2:
				pass
			elif argc == 3:
				pass
			else:
				print 'Bad usage, branch target or branch source target'
		else:
			print 'Matched none. Your command is incorrect.'
			return 2
	return 0

def main(argv=None):
	if argv is None:
		argv = sys.argv
		try:
			try:
				opts, args = getopt.getopt(argv[1:],"h",["help"])
			except getopt.getopt, msg:
				raise Usage(msg)
		except Usage, err:
			print >> sys.stderr, err.msg
			print >> sys.stderr, "for help use --help"
			return 2
		result = processArgs(len(args), args)
		if result == 2:
			helpUserMakeDecision()
		return result

if __name__ == "__main__":
	sys.exit(main())
