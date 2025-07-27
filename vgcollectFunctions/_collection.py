import requests
import colorama
import os
import time
import re
from ._config import Config
class collection(object):
     show_notes = False
     database_path = "/var/db/vgcollect/cache.csv"
     use_local = False
     debug = False

     def __init__(self, use_local, show_notes, debug=False):
          self.debug = debug
          self.use_local = use_local
          self.show_notes = show_notes
          self.loadCollection(use_local)

     def loadCollection(self, use_local):
          auth = Config()

          login_url = "https://vgcollect.com/login/authenticate"
          export_url = "https://vgcollect.com/settings/export/collection"


          values = {'username': auth.username,
                    'password': auth.password}

          # If we are using the local cache, we want to skip trying to pull in the latest data
          if (use_local == True and not self.getFileModificationTime()):
               file = open(self.database_path, "r")
               self.collection_local = file.read()
               file.close()
               self.use_local = True
               self.debugLog("Using local cached file database")
               return

          self.debugLog("Refreshing local database from vgcollect")
          session = requests.Session()

          post = session.post(login_url, data=values)
          self.collection = session.get(export_url)

          # Dump the data into a cache, this can be used laster with the "use_local" flag to speed up searching
          # At the expense at using old data
          file = open(self.database_path, "w")
          for line in self.collection.iter_lines():
               file.write(str(line) + "\n")
               #file.write(str(line))
          file.close()

          # Now re-read the collection file
          file = open(self.database_path, "r")
          self.collection_local = file.read()
          file.close()

          session.close()

     # The purpose of this function is to replace special characters and
     # convert all searching to lower case for easier searching
     def fixStringInput(self, string):
          string = (string.replace('\\xc3\\xa9', 'e') # For Pokemon é
                          .replace('\\\'', '')  # Replaces \' with nothing for easier searching
                          .replace('&amp;', '&') # Fixing &
                          .replace(':', '') # Remove colins for search
                          .replace('-', '') # Remove dash for search
                          .replace('.', '') # Remove periods
                          .replace(' ', '') # Remove spaces
          )
          return string.lower()

     # This will fix any string that is outputted
     def fixStringOutput(self, string):
          string = (string.replace('\\xc3\\xa9', 'é') # For Pokemon é
                          .replace('\\\'', '\'') # Replaces \' with '
                          .replace('&amp;', '&') # Fixing &
          )
          return string
     
     def debugLog(self, message):
          if (self.debug == True):
               print("[Debug] " + message)

     def checkBox(self, string):
          from colorama import Fore
          if (string == "Yes"):
               return Fore.GREEN + "✓" 
          else:
               return Fore.RED + "✘"

     # This fucntion will return true if the current database is 1 day out of date, false if it isn't
     def getFileModificationTime(self):
          modification_time = os.path.getmtime(self.database_path)   
          epoch_time = int(time.time())
          # print("hello:"+epoch_time)
          # print(modification_time)
          if (epoch_time - modification_time > 86400):
               self.debugLog("Local cached file is out of date")
               return True
          else:
               return False

     def fixStringOutputConsole(self,string):
          string = (string.replace('Nintendo Entertainment System ', 'NES ')) # Shortens the console NES
          string = (string.replace('Super Nintendo ', 'SNES ')) # Shortens the console SNES
          string = (string.replace('Game Boy Advance ', 'GBA ')) # Shortens the console GBA
          string = (string.replace('Nintendo Switch ', 'Switch ')) # Shortens the console Switch
          string = (string.replace('PlayStation Portable ', 'PSP ')) # Shortens the console PSP
          string = (string.replace('PlayStation 2 ', 'PS2 ')) # Shortens the console PS2
          string = (string.replace('PlayStation 2 ', 'PS2 ')) # Shortens the console PS2
          string = (string.replace('PlayStation 3 ', 'PS3 ')) # Shortens the console PS3
          string = (string.replace('PlayStation 4 ', 'PS4 ')) # Shortens the console PS4
          string = (string.replace('PlayStation 5 ', 'PS5 ')) # Shortens the console PS5
          string = (string.replace('PlayStation 6 ', 'PS6 ')) # Shortens the console PS6
          string = (string.replace('PlayStation Network ', "PSN ")) # Shortens the console PSN
          string = (string.replace('Sega Genesis/Mega Drive Accessory', "Sega Genesis Accessory "))
          string = (string.replace('Skylanders Figures/Traps/Vehicles', "Skylanders "))
          string = (string.replace('Super Nintendo/Super Famicom Accessory', "SNES Accessory"))
          return string

     def getResults(self, collection, query, show_missing_case):
          self.debugLog("User query is: " + query)

          # First, lets aphapatize the list, first by console, then by title
          collection_alphabetized = []
          if (show_missing_case):
               fixed_query = self.fixStringInput(query)
               
               if (fixed_query.startswith("ps")):
                    if (fixed_query == "ps" or fixed_query == "ps1"):
                         fixed_query = "playstation"
                    else:
                         fixed_query = "playstation" + fixed_query[-1:]
                         
                    self.debugLog("User query changing to: " + fixed_query)
               
               for line in collection:
                    console = self.fixStringOutputConsole(self.fixStringInput(str(line).split("\",\"")[2])).split("[")[0]
                    
                    if (str(line).split("\",\"")[5] == "No"):

                         # Lets try to get a more exact result
                         add_entry = False
                         if (console == fixed_query):
                              add_entry = True
                         elif (self.fixStringInput(self.fixStringOutputConsole(str(line).split("\",\"")[2].split("[")[0])) == fixed_query):
                              add_entry = True
                         elif (console.replace("sega", "") == fixed_query): # try removing "sega"
                              add_entry = True

                         if (add_entry):
                              self.debugLog("console: " + console)
                              self.debugLog("query: " + fixed_query)
                              collection_alphabetized.append(
                                   [
                                        self.fixStringOutputConsole(str(line).split("\",\"")[2]), # Console
                                        self.fixStringOutput(str(line).split("\",\"")[1]), # Title\
                                        self.checkBox(str(line).split("\",\"")[4]), # Cart
                                        self.checkBox(str(line).split("\",\"")[5]), # Box
                                        self.checkBox(str(line).split("\",\"")[6]), # Manual
                                        str(line).split("\",\"")[8], # Price
                                        str(line).split("\",\"")[3], # Notes
                                   ])
          
          elif (show_missing_case == False):
               for line in collection:
                    if (self.fixStringInput(str(line)).find(self.fixStringInput(self.fixStringInput(query))) != -1):
                         collection_alphabetized.append(
                              [
                                   self.fixStringOutputConsole(str(line).split("\",\"")[2]), # Console
                                   self.fixStringOutput(str(line).split("\",\"")[1]), # Title\
                                   self.checkBox(str(line).split("\",\"")[4]), # Cart
                                   self.checkBox(str(line).split("\",\"")[5]), # Box
                                   self.checkBox(str(line).split("\",\"")[6]), # Manual
                                   str(line).split("\",\"")[8], # Price
                                   str(line).split("\",\"")[3], # Notes
                              ])
          
          collection_alphabetized.sort()

          result1 = []
          result2 = []

          index = 0
          previous_console = ""
          console = ""
          for line in collection_alphabetized:
               if (index == 0):
                    console = line[0]
               if (line[0] != previous_console):
                    result1.append([
                         line[0],
                         "",
                         "",
                         "",
                         "",
                    ])
               else:
                    console = ""
               index = index + 1

               previous_console = line[0]

               result1.append(
                    [
                         "  " + line[1], # Title\
                         line[2], # Cart
                         line[3], # Box
                         line[4], # Manual
                         line[5], # Price
                    ])


               result2.append(
                    [
                         "    " + line[6], # Notes
                         "",
                         "",
                         "",
                         "",
                    ])

          # Add the header to result1
          from colorama import Fore
          result1.insert(0, ["  Title", Fore.WHITE + "Cart" , Fore.WHITE + "Box" , Fore.WHITE + "Manual" , Fore.WHITE + "Cost    "])
          
          return result1, result2

     def search(self, query, show_missing_case=False, refresh=False):

          result1, result2 = self.getResults(self.collection_local.splitlines(), query, show_missing_case)

          # Format the output into a table
          from colorama import init, Fore, Back, Style
          init(autoreset=True)
          
          color_cycle = False
          header_printed1 = False

          lens = []
          lens2 = []

          for col in zip(*result1):
               lens.append(max([len(v) for v in col]))
          for col in zip(*result2):
               lens2.append(max([len(v) for v in col]))
          
          index = 0

          # The intention here is to figure out how wide each column is. Since we moved the notes & price column
          # to the next line, we need to figure out whether the title or notes field is the longest column
          if (len(lens2) != 0 and self.show_notes == True):
               for l in lens:
                    if (l < lens2[index]):
                         lens[index] = lens2[index]
                    index = index + 1
          
          format = "  ".join(["{:<" + str(l) + "}" for l in lens])
          index = -1

          for row in result1:
               
               if (not header_printed1):
                    print(Fore.WHITE + Back.BLUE + format.format(*row))
                    header_printed1 = True
               elif (row[2] == ""): # must be a platform header
                    print()
                    # We need to add junk ANSCI colors to the rest of the empty columns
                    # If we dont do this, the background row will extend past
                    for addjunk in range(1, 5):
                         row[addjunk] = Fore.BLACK + ""
                    
                    print(Fore.BLACK + Back.LIGHTBLUE_EX + format.format(*row))
                    continue
               elif (color_cycle):
                    row[4] = Fore.WHITE + row[4]
                    print(Fore.WHITE + Back.LIGHTBLACK_EX + format.format(*row))
                    if (self.show_notes):
                         # We need to add junk ANSCI colors to the rest of the empty columns
                         # If we dont do this, the background row will extend past
                         for addjunk in range(1, 5):
                              result2[index][addjunk] = Fore.WHITE + ""

                         print(Fore.WHITE + Back.LIGHTBLACK_EX + format.format(*result2[index]))
               else:
                    row[4] = Fore.BLACK + row[4]
                    print(Fore.BLACK + Back.LIGHTWHITE_EX  + format.format(*row))
                    if (self.show_notes):

                         # We need to add junk ANSCI colors to the rest of the empty columns
                         # If we dont do this, the background row will extend past
                         for addjunk in range(1, 5):
                              result2[index][addjunk] = Fore.BLACK + ""

                         print(Fore.BLACK + Back.LIGHTWHITE_EX  + format.format(*result2[index]))
               color_cycle = not color_cycle
               index = index+1

     def backup(self):
          #print(str(self.collection_local).replace('\n', ''))
          output = re.sub(',\'$', '', str(self.collection_local).replace(',\'\nb\'', '\n'))
          print(output)
