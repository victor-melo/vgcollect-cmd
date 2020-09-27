import configparser

class Config:
  username = ""
  password = ""

  def __init__(self):
      config = configparser.ConfigParser()
      config.read('vgcollect.cfg')
      self.username = config['AUTH']['Username']
      self.password = config['AUTH']['Password']
  
  def Username(self):
    return self.username

  def Password(self):
    return self.password
