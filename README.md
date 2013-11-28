CSC444 Assignment 2: Source Code Management System
==============
*View the [source of this content](http://github.com/zhwzh308/csc444asst2).*

Description
-------------------------
1. The project git directory contains the implementation of ASST2.
2. The scope of this project is to satisfy the specification ONLY.
3. We recommand that you do not use this for your own project source management, because it has dependancy of sqlite3.
4. The command line interface takes from 1 to n arguments and the layout is specified by the following section
5. DEMO

Specification
-------------------------
# 1 argument
```$ python asst2.py```

- This will return the unsupported message. While advising user to use specific commands.
- So that user can learn from the message, what are the available operations about this program.

# 2 arguments
```
    $ python asst2.py init
    $ python asst2.py status
    $ python asst2.py help
```
- init: initialize the directory to enable SCM
- status: prompt user whether SCM is enabled or not
- help: display help message
- commit: commit change.

# 3 or more arguments
```
    $ python asst2.py add *
    $ python asst2.py diff
```
- add files; add 1 or more files. Currently only one file is required to add
