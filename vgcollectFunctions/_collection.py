import requests
import colorama
from ._config import Config
class collection(object):

     def __init__(self, use_local):
          self.loadCollection(use_local)

     def loadCollection(self, use_local):
          print("use local is", use_local)
          auth = Config()

          login_url = "https://vgcollect.com/login/authenticate"
          export_url = "https://vgcollect.com/settings/export/collection"


          values = {'username': auth.username,
                    'password': auth.password}

          # If we are using the local cache, we want to skip trying to pull in the latest data
          if (use_local):
               file = open("cache.csv", "r")
               self.collection_local = file.read()
               return

          session = requests.Session()

          post = session.post(login_url, data=values)
          self.collection = session.get(export_url)

          # Dump the data into a cache, this can be used laster with the "use_local" flag to speed up searching
          # At the expense at using old data
          file = open("cache.csv", "w")
          for line in self.collection.iter_lines():
               file.write(str(line) + "\n")
               #file.write(str(line))
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

     def checkBox(self, string):
          if (string == "Yes"):
               return "✓"
          else:
               return "✘"

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

     def search(self, query, use_local):
          
          result1 = [["Platform", "Title", "Cart", "Box", "Manual"], ["----","----", "----", "----", "----"]]
          result2 = []
          if (use_local == False):
               for line in self.collection.iter_lines():
                    if (self.fixStringInput(str(line)).find(self.fixStringInput(self.fixStringInput(query))) != -1):
                         result1.append(
                              [
                                   self.fixStringOutputConsole(str(line).split("\",\"")[2]), # Console
                                   self.fixStringOutput(str(line).split("\",\"")[1]), # Title\
                                   self.checkBox(str(line).split("\",\"")[4]), # Cart
                                   self.checkBox(str(line).split("\",\"")[5]), # Box
                                   self.checkBox(str(line).split("\",\"")[6]), # Manual
                              ])

                         result2.append(
                              [
                                   str(line).split("\",\"")[3], # Notes
                                   str(line).split("\",\"")[8], # Price
                                   "",
                                   "",
                                   ""
                              ])
          else:
               # If the person added the use_local flag, search the local cache
               for line in self.collection_local.splitlines():
                    if (self.fixStringInput(str(line)).find(self.fixStringInput(self.fixStringInput(query))) != -1):
                         result1.append(
                              [
                                   self.fixStringOutputConsole(str(line).split("\",\"")[2]), # Console
                                   self.fixStringOutput(str(line).split("\",\"")[1]), # Title
                                   self.checkBox(str(line).split("\",\"")[4]), # Cart
                                   self.checkBox(str(line).split("\",\"")[5]), # Box
                                   self.checkBox(str(line).split("\",\"")[6]), # Manual
                              ])
                         result2.append(
                              [
                                   "Cost: " + str(line).split("\",\"")[8], # Price
                                   str(line).split("\",\"")[3], # Notes
                                   "",
                                   "",
                                   ""
                              ])
                         



          # Format the output into a table
          from colorama import init, Fore, Back, Style
          init(autoreset=True)
          
          color_cycle = False
          header_printed1 = False
          header_printed2 = False

          lens = []
          lens2 = []

          for col in zip(*result1):
               lens.append(max([len(v) for v in col]))
          for col in zip(*result2):
               lens2.append(max([len(v) for v in col]))
          
          index = 0

          # The intention here is to figure out how wide each column is. Since we moved the notes & price column
          # to the next line, we need to figure out whether the title or notes field is the longest column
          if (len(lens2) != 0):
               for l in lens:
                    if (l < lens2[index]):
                         lens[index] = lens2[index]
                    index = index + 1
          

          format = "  ".join(["{:<" + str(l) + "}" for l in lens])
          index = -2

          for row in result1:
               #print (row)
               if (not header_printed1):
                    print(Fore.BLACK + Back.LIGHTCYAN_EX + format.format(*row))
                    header_printed1 = True
               elif (not header_printed2):
                    print(Fore.WHITE + Back.LIGHTBLACK_EX + format.format(*row))
                    header_printed2 = True
               elif (color_cycle):
                    print(Fore.WHITE + Back.LIGHTBLACK_EX + format.format(*row))
                    print(Fore.WHITE + Back.LIGHTBLACK_EX + format.format(*result2[index]))
               else:
                    print(Fore.BLACK + Back.CYAN  + format.format(*row))
                    print(Fore.BLACK + Back.CYAN  + format.format(*result2[index]))
               color_cycle = not color_cycle
               index = index+1

     def backup(self):
          print(str(self.collection.content).replace('\\n', '\n'))
