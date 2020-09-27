import requests
from ._config import Config
class collection(object):

     def __init__(self):
          print("Loading Collection")
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
     def clear(self):
          print("test123")

     # The purpose of this function is to replace special characters and
     # convert all searching to lower case for easier searching
     def fixStringInput(self, string):
          test = string.replace('\\xc3\\xa9', 'e') # For Pokemon é
          return test.lower()

     # This will fix any string that is outputted
     def fixStringOutput(self, string):
          test = string.replace('\\xc3\\xa9', 'é') # For Pokemon é
          return test

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

          lens = []
          for col in zip(*result):
               lens.append(max([len(v) for v in col]))
          format = "  ".join(["{:<" + str(l) + "}" for l in lens])
          for row in result:
               print(format.format(*row))
