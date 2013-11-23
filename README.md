CSC444 Assignment 2: Source Code Management System
==============
*View the [source of this content](http://github.github.com/zhwzh308/csc444asst2).*

Description
-------------------------
The project git directory contains the implementation of ASST2.
The scope of this project is to satisfy the specification ONLY.
We recommand that you do not use this for your own project source management, because it has dependancy of sqlite3.

The command line interface takes from 1 to n arguments and lays out as this:

Specification
-------------------------
--- 1 argument ---
python asst2.py
- This will return the unsupported message. While advising user to use specific commands.
- So that user can learn from the message, what are the available operations about this program.

--- 2 arguments ---
python asst2.py cwd
python asst2.py status
python asst2.py info
python asst2.py list
- This offers user information under the cwd, whether the status of this directory is under SCM or not.

--- 3 or more arguments ---
python asst2.py add *
python asst2.py del *
- add and delete files; they are used against 1 or more files, whose filenames are
- seperated by whitespace. For the del, the filenames are passed first through the filter, to
- see whether they present under SCM. For add, non existent files are not added because it is nonsafe
- unless the author of that file actually commits.
