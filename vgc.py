#!/bin/python3

import vgcollectFunctions._collection
import sys


 
total = len(sys.argv)
cmdargs = sys.argv


arg_search = ""
search = False
backup = False
use_local = False

for num in range(total):
  if num == 0:
    continue
  
  if search == True:
    search = False
    arg_search = cmdargs[num]
    continue

  if cmdargs[num] == 'use_local':
    use_local=True

  if cmdargs[num] == 'search':
    search = True
    continue

  elif cmdargs[num] == 'backup':
    backup = True
    break

f = vgcollectFunctions._collection.collection(use_local)

if (arg_search != ""):
  f.search(arg_search, use_local)
elif (backup == True):
  f.backup()


