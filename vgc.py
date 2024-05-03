#!/bin/python3

import vgcollectFunctions._collection
import sys


 
total = len(sys.argv)
cmdargs = sys.argv


arg_search = ""
search = False
backup = False
use_local = False
show_notes = False

for num in range(total):
  if num == 0:
    continue
  
  if search == True:
    search = False
    arg_search = cmdargs[num]
    continue

  if cmdargs[num] == 'use_local':
    use_local=True

  if cmdargs[num] == 'show_notes':
    show_notes=True

  if cmdargs[num] == 'search':
    search = True
    continue

  elif cmdargs[num] == 'backup':
    backup = True
    break

  elif cmdargs[num] == 'help' or cmdargs[num] == 'h' or cmdargs[num] == '-h':
    print ("Usage:")
    print ("")
    print ("  search \"<query>\" - Search your collection with a query")
    print ("  use_local        - This will only search the local cache instead of calling out to vgcollect")
    print ("  show_notes       - Show the notes field for each games shown")
    print ("  help             - Show this page")
    print ("\n")
    print ("  Example usage: ./vgc.py use_local search \"mario\"")
    print ("")
    quit()

f = vgcollectFunctions._collection.collection(use_local, show_notes)

if (arg_search != ""):
  f.search(arg_search, use_local)
elif (backup == True):
  f.backup()


