import configparser
import os

class Config:
  username = ""
  password = ""

  def __init__(self):
      config = configparser.ConfigParser()
      config.read(os.path.expanduser( '~' ) + '/.config/vgcollect/vgcollect.cfg')

      try:
        self.username = config['AUTH']['Username']
        self.password = config['AUTH']['Password']
      except:
        print ("Invalid user/password or cannot read config file")
        quit()
  
  def Username(self):
    return self.username

  def Password(self):
    return self.password
