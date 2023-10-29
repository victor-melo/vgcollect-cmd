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
          )
          return string.lower()

     # This will fix any string that is outputted
     def fixStringOutput(self, string):
          string = (string.replace('\\xc3\\xa9', 'é') # For Pokemon é
                          .replace('\\\'', '\'') # Replaces \' with '
                          .replace('&amp;', '&') # Fixing &
          )
          return string

     def fixStringOutputConsole(self,string):
          string = (string.replace('Nintendo Entertainment System ', 'NES ') # Shortens the console NES
          )
          return string

     def search(self, query, use_local):
          
          result = [["Console", "Title", "Cart", "Box", "Manual", "Notes", "Cost"], ["---","---", "---", "---", "---", "---", "---"]]

          if (use_local == False):
               for line in self.collection.iter_lines():
                    if (self.fixStringInput(str(line)).find(self.fixStringInput(self.fixStringInput(query))) != -1):
                         result.append(
                              [
                                   self.fixStringOutputConsole(str(line).split("\",\"")[2]), # Console
                                   self.fixStringOutput(str(line).split("\",\"")[1]), # Title\
                                   str(line).split("\",\"")[4], # Cart
                                   str(line).split("\",\"")[5], # Box
                                   str(line).split("\",\"")[6], # Manual
                                   str(line).split("\",\"")[3], # Notes
                                   str(line).split("\",\"")[8], # Price
                              ])
          else:
               # If the person added the use_local flag, search the local cache
               for line in self.collection_local.splitlines():
                    if (self.fixStringInput(str(line)).find(self.fixStringInput(self.fixStringInput(query))) != -1):
                         result.append(
                              [
                                   self.fixStringOutputConsole(str(line).split("\",\"")[2]), # Console
                                   self.fixStringOutput(str(line).split("\",\"")[1]), # Title
                                   str(line).split("\",\"")[4], # Cart
                                   str(line).split("\",\"")[5], # Box
                                   str(line).split("\",\"")[6], # Manual
                                   str(line).split("\",\"")[3], # Notes
                                   str(line).split("\",\"")[8], # Price
                              ])
                         



          # Format the output into a table
          from colorama import init, Fore, Back, Style
          init(autoreset=True)
          
          color_cycle = False
          header_printed = False

          lens = []
          for col in zip(*result):
               lens.append(max([len(v) for v in col]))
          format = "  ".join(["{:<" + str(l) + "}" for l in lens])
          for row in result:
               if (not header_printed):
                    print(Fore.BLACK + Back.LIGHTCYAN_EX + format.format(*row))
                    header_printed = True
               elif (color_cycle):
                    print(Fore.WHITE + Back.LIGHTBLACK_EX+ format.format(*row))
               else:
                    print(Fore.BLACK + Back.CYAN  + format.format(*row))
               color_cycle = not color_cycle



     def backup(self):
          print(str(self.collection.content).replace('\\n', '\n'))
