import vgcollectFunctions._collection
import sys

f = vgcollectFunctions._collection.collection()
 
total = len(sys.argv)
cmdargs = sys.argv


arg_search = ""
search = False
backup = False

for num in range(total):
  if num == 0:
    continue

  if search == True:
    search = False
    arg_search = cmdargs[num]
    continue

  if cmdargs[num] == 'search':
    search = True
    continue
  elif cmdargs[num] == 'backup':
    backup = True
    break

if (arg_search != ""):
  f.search(arg_search)
elif (backup == True):
  f.backup()


