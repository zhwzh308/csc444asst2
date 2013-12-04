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
	# Return True after line.decode.

# Check if a file is ASCII
def isAsciiFile(filename):
	if fileExist(filename):
		f = open(filename, 'r')
		for line in f.readlines():
			if not isAscii(line):
				f.close()
				return False
		f.close()
		return True
	else:
		return False

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
		# Only if the branch file exist.
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
		return os.path.isdir(foldername)
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
		# Safe to assume there is .scm.
		files = os.listdir('.scm')
		cwdfiles = os.listdir(os.getcwd())
		for item in files:
			# return the first one is sufficient
			if item in cwdfiles:
				return item
	else:
		return None

# Support Init command
def scmInit(branch='main'):
	# Default behavior: initialize main branch.
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
				print 'adding',filename
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
			# If we want a specific version
			for item in os.listdir('.scm'):
				if branch in item:
					if version in item:
						# Both branch name and version string is present in the file.
						return item
		else:
			# want the latest version
			baseversion = '1'
			files = os.listdir('.scm')
			if len(files)>1:
				qualifier = '.'+branch+'_'
				toreturn = files[1]
				for item in files:
					if qualifier in item:
						if int(baseversion) < int(getVersionString(item)):
							toreturn = item
			else:
				toreturn = files[0]
			return toreturn
	else:
		print 'Folder is not under SCM.'
		return '0'

def getVersionString(filename):
	localtmp = filename.split('_')
	if (len(localtmp)>1):
		return localtmp[1]
	else:
		return '0'

def checkoutFile(branch='main', version='0'):
	if folderUnderControl():
		version = getFileName(branch, version)
		filename = os.path.join('.scm', getFileName(branch,version))
		if fileExist(filename):
			fw = open(discoverSCMFile(),'w')
			fr = open(filename,'r')
			fw.writelines(fr.readlines())
			fw.close()
			fr.close()
		else:
			print 'checkout file failed at',branch,'version',version
	else:
		print 'initialize SCM first.'

def commitFile(branch='main'):
	# since version number is assigned to the
	# commit, the user is not allowed to specify
	# the number
	if folderUnderControl():
		newfile = discoverSCMFile()
		oldfile = '.scm/'+getFileName(branch)
		#print 'comparing with',oldfile
		if isSameFile(newfile, oldfile):
			print 'Nothing to commit.'
		else:
			suffix = '.'+branch+'_'+str(int(getVersionString(getFileName(branch)))+1)
			# suffix for next version file.
			writefile = os.path.join('.scm',newfile)+suffix
			touch(writefile)
			readfile = open(newfile,'r')
			file1 = open(writefile,'w')
			file1.writelines(readfile.readlines())
			readfile.close()
			file1.close()
			print 'Commit success'
	else:
		print 'You cannot commit, the scm is not initialized.'

def branchCreate(branch='main'):
	# assume the command was ran to confirm branch is not there.
	touch(os.path.join('.scm',branch))

def branchGenerate(branchX='main',branchY='default'):
	if os.path.exists(os.path.join('.scm',branchY)):
		print "Branch",branchY,'exist'
	else:
		branchCreate(branchY);
	suffix = '.'+branch+'_1'
	source = os.path.join('.scm',discoverSCM())
	dest = source+suffix
	touch(os.path.join('.scm', dest))
	f1= open((os.path.join('.scm',source)),'r')
	f2= open((os.path.join('.scm',dest)),'w')
	f2.writelines(f1.readlines())
	f1.close()
	f2.close()
	print 'Branched file',source,'from main to',branchY


def comment(comment='',branch='main'):
	if comment == '':
		print  'on',branch,'- no comment'
	else:
		print 'comment on',branch,'-',comment

# Create diff helper if needed.

def diffFile():
	if folderUnderControl():
		newfile = discoverSCMFile()
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
	Usage:
	python asst2.py help - print this message.
	python asst2.py init - Initiate SCM, create main.
	python asst2.py add - return if any file is under SCM
	python asst2.py add [filename] - Source control [filename]
	python asst2.py commit branch comment - Commit the change, branch must be specified, and comment are optional.
	python asst2.py checkout - checkout version from branch
	python asst2.py list - list all files in all branches. 
	python asst2.py branch X- fork a new branch named X based on main
	python asst2.py branch X Y- fork a new branch Y based on X.
	python asst2.py diff - Diff file which is under SCM
	'''

def listSCM():
	filename = discoverSCMFile()
	if filename == None:
		print 'Please initialized directory first.'
	else:
		qualifier = filename+'.'
		print 'file:',filename
		for item in os.listdir('.scm'):
			if qualifier in item:
				print 'branch:', item.split('_')[0].split('.')[2], 'version:', item.split('_')[1]

def processArgs(argc, argv):
	# print argc, argv argv starts after python *.py, argv[0] would be the command
	if argc == 0:
		return 2
	else:
		command = argv[0]
		if command == 'init':
			if argc == 1:
				# default case: get main branch running.
				scmInit()
			elif argc==2:
				# init a branch.
				scmInit(branch=argv[1])
			else:
				print 'Bad usage, init, or init _branch_'
		elif command == 'add':
			if argc == 2:
				# "add filename"
				addFile(argv[1])
			else:
				print 'Bad usage, add filename'
		elif command == 'commit':
			if argc == 1:
				# commit, no branch nor comment
				commitFile()
			elif argc == 2:
				# commit file with branch
				commitFile(branch=argv[1])
			elif argc == 3:
				# commit file with branch and comment.
				commitFile(branch=argv[1])
				comment(argv[1],argv[2])
			else:
				print 'Bad usage, commit [branch] [comment]'
		elif command == 'checkout':
			if argc == 2:
				# Checkout newest main
				checkoutFile()
			elif argc == 3:
				# Checkout a version from main.
				checkoutFile(version=argv[1])
				print 'Version',argv[1],'from main checked out.'
			elif argc == 4:
				# Checkout a version
				checkoutFile(branch=argv[1],version=argv[2])
				print 'Version',argv[1],'from', argv[2], 'checked out.'
			else:
				print 'Bad usage, checkout # or checkout branch #'
		elif command == 'list':
			if argc == 1:
				listSCM()
			elif argc == 2:
				listSCM(argv[1])
			else:
				print 'Bad usage, list [branch]'
		elif command == 'branch':
			if argc == 1:
				print 'Please specify the branch name'
			elif argc == 2:
				if branchExist(argv[1]):
					print 'branch exist!'
				else:
					branchCreate(argv[1])
			elif argc == 3:
				if branchExist(argv[1]):
					if branchExist(argv[2]):
						print 'giving up branch:',argv[2],' does not exist.'
					else:
						diffFile()
						branchCreate(argv[1],argv[2])
						checkoutFile()
				else:
					print 'Fault: not able to branch from',argv[1]
			else:
				print 'Bad usage, branch _target_ or branch _source_ _target_'
		elif command == 'diff':
			if argc == 1:
				diffFile()
			else:
				print 'Diff is an experimental funtionality. It is helpful to generate branches.'
		else:
			print 'Matched none. Your command is incorrect.'
			return 2
	return 0

def main(argv=None):
	# You calling main with argv. It is not expected
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
	else:
		print 'Unexpected usage.'

if __name__ == "__main__":
	sys.exit(main())
