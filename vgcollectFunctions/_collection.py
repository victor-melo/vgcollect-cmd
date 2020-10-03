import requests
from ._config import Config
class collection(object):

     def __init__(self):
          self.loadCollection()

     def loadCollection(self):
          auth = Config()

          login_url = "https://vgcollect.com/login/authenticate"
          export_url = "https://vgcollect.com/settings/export/collection"


          values = {'username': auth.username,
                    'password': auth.password}

          session = requests.Session()

          post = session.post(login_url, data=values)
          self.collection = session.get(export_url)
          
          session.close()

     # The purpose of this function is to replace special characters and
     # convert all searching to lower case for easier searching
     def fixStringInput(self, string):
          string = string.replace(
               '\\xc3\\xa9', 'é').replace( # For Pokemon é
               '\\\'', '') # Replaces \' with nothing for easier searching
          return string.lower()

     # This will fix any string that is outputted
     def fixStringOutput(self, string):
          string = string.replace(
               '\\xc3\\xa9', 'é').replace( # For Pokemon é
               '\\\'', '\'') # Replaces \' with '
          return string

     def search(self, query):
          
          result = [["Console", "Title", "Notes", "Cost"], ["========","========", "========", "========"]]
          for line in self.collection.iter_lines():
               if (self.fixStringInput(str(line)).find(self.fixStringInput(self.fixStringInput(query))) != -1):
                    result.append(
                         [str(line).split("\",\"")[2], # Console
                         self.fixStringOutput(str(line).split("\",\"")[1]), # Title
                         str(line).split("\",\"")[3], # Notes
                         str(line).split("\",\"")[8],]
                         )

          # Format the output into a table
          lens = []
          for col in zip(*result):
               lens.append(max([len(v) for v in col]))
          format = "  ".join(["{:<" + str(l) + "}" for l in lens])
          for row in result:
               print(format.format(*row))

     def backup(self):
          print(str(self.collection.content).replace('\\n', '\n'))
