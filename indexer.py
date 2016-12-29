"""PeARS indexer

Usage:
indexer.py --history=10
indexer.py --history=10 --cluster
indexer.py --file=NAME
indexer.py --file=NAME --cluster
indexer.py (-h | --help)
indexer.py --version

Options:
-h --help     Show this screen.
--version     Show version.
--history=NUM Number of pages of local history to index
--file=NAME   Name of url file to index
--cluster
"""

from pears.indexer import retrieve_raw_data,hierarchClustering,mkLocalProfile
from docopt import docopt
import os, sys


if __name__=="__main__":
  args = docopt(__doc__, version='PeARS indexer 0.1')
  if args["--history"]:
    retrieve_raw_data.runScript("history", args["--history"])
    if args["--cluster"]:
      hierarchClustering.runScript(0.5)
  if args["--file"]:
    retrieve_raw_data.runScript("file", args["--file"])
    if args["--cluster"]:
      hierarchClustering.runScript(0.5)

  mkLocalProfile.runScript()
