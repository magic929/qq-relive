import os
import configparser

baseDir = './config/'

class ConfigSet():
    def __init__(self):
        config = configparser.ConfigParser()
        mode = os.environ.get('MODE')
        print(mode)
        if not mode:
            return False
        config.read(baseDir+mode+'.ini')
        self.mongodb_add1 = config["MongDB"]["add1"]
        self.mongodb_add2 = config['MongDB']["add2"]
        self.mongdb_user = config['MongDB']['user']
        self.mongodb_pass = config['MongDB']['pass']
        self.db_relive = config['DB']['relive']
        self.collection_boss = config['collection']['boss']
        self.alias_reliveqq = config['ALIAS']['reliveqq']