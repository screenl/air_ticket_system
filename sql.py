import pymysql
import json
import os

config = json.load(open(f'{os.path.split(os.path.realpath(__file__))[0]}/config.json'))

class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)
    
@Singleton
class SQLConnection():
    def __init__(self):
        self.conn = pymysql.connect(host=config['host'],
                                user=config['user'],
                                password=config['password'],
                                database='air_ticket',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
        print('connected!')
        
