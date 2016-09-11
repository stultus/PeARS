#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import platform
import subprocess

def setup():
    # Identify the type of operating system for install packages
    OS = platform.dist()[0].lower()

    if OS == "fedora" or OS == "redhat":
        install = "sudo yum install "
    elif OS == "ubuntu" or OS == "debian":
        install = "sudo apt-get install "
    else:
        print "Automatic installation is not available on your system.\n" \
              "Please install the system using a description in the 'README.md'"
        exit(1)

    # It was installed packages: 'pip' and 'virtualenv'
    with open("/dev/null", "a") as null:
        # If the command 'which' the back 1, the package is not installed
        if subprocess.call(["which", "pip"], stdout=null) is 1:
            os.system(install + "python-pip" + " -y")

        if subprocess.call(["which", "virtualenv"], stdout=null) is 1:
            os.system(install + "virtualenv" + " -y")

    # Configure virtual environment ('virtualenv')
    if not hasattr(sys, 'real_prefix'):
        if not os.path.isdir('pears_env'):
            os.system("virtualenv pears_env")

    # Installing dependencies
    os.system("cd pears_env/bin/ ; sudo -H pip2 install -r ../../requirements.txt")
    os.system("cd ../../")

    # Get the semantic space
    os.system("wget http://clic.cimec.unitn.it/~aurelie.herbelot/openvectors.dump.bz2")
    os.system("./uncompress_db.py openvectors.dump.bz2")

def isInt(n):
    '''Check that a string is an int'''
    try:
        int(n)
        return True
    except ValueError:
        return False

def index_browser_history():
    num_pages=50
    if not os.path.isdir("./local-history"):
      os.mkdir("./local-history/")

    user_in=raw_input(
    "\nHi, welcome to the PeARS Firefox history analyser.\n\
    This program allows you to index the pages in your Web history\n\
    to subsequently search them with the PeARS search engine.\n\n\
    IMPORTANT: Please note that the analyser has to retrieve every page\n\
    it indexes from the Web, so if you have concerns about processing time,\n\
    bandwidth, or making too many calls to a particular domain, please\n\
    use the program carefully. By default, the program is set to only\n\
    index the 50 pages you visited most.\n\nWhat would you like to do?\n\
        a) yeah, index those 50 pages (y)\n\
        b) get me out of here (x)\n\
        c) index this number of pages (enter a number)\n")

    user_in=user_in.strip()

    while user_in not in ["y","x"] and not isInt(user_in):
      user_in=raw_input("Please press 'y', 'x', or enter a number.")

    if isInt(user_in):
            num_pages=int(user_in)
    if user_in=="x":
            sys.exit()

    retrieve_raw_data.runScript(num_pages,"./local-history/documents.txt")

if __name__=="__main__":
    setup()


    from pears.indexer import retrieve_raw_data

    index_browser_history()
