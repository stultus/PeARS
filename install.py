#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import platform
import subprocess
from indexer import index_browser_history

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

    # Installing dependencies
    os.system("sudo pip install -r requirements.txt")

    # Get the semantic space
    os.system("wget http://clic.cimec.unitn.it/~aurelie.herbelot/openvectors.dump.bz2")
    os.system("./uncompress_db.py openvectors.dump.bz2")


if __name__=="__main__":
    setup()
    print "Now please run the indexer. Run python ./indexer.py -h for help."
