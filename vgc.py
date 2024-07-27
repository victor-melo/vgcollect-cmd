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
show_missing_case = False

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

  if cmdargs[num] == 'cases':
    show_missing_case=True

  if cmdargs[num] == 'search':
    search = True
    continue

  elif cmdargs[num] == 'backup':
    backup = True
    break

  elif cmdargs[num] == 'help' or cmdargs[num] == 'h' or cmdargs[num] == '-h' or cmdargs[num] == '--help':
    print ("Usage:")
    print ("")
    print ("  search \"<query>\" - Search your collection with a query")
    print ("  use_local        - This will only search the local cache instead of calling out to vgcollect")
    print ("  show_notes       - Show the notes field for each games shown")
    print ("  cases            - Show games with missing cases, your search query becomes console search")
    print ("  help             - Show this page")
    print ("\n")
    print ("  Example of searching for mario games using only the local cache")
    print ("  Example usage: ./vgc.py use_local search \"mario\"")
    print ("")
    print ("  Example of searching for all gamecube games with missing cases")
    print ("  Example usage: ./vgc.py cases search \"GameCube\"")
    print ("")
    quit()

f = vgcollectFunctions._collection.collection(use_local, show_notes)

if (arg_search != ""):
  f.search(arg_search, use_local, show_missing_case)
  
elif (backup == True):
  f.backup()


