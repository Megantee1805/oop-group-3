from datetime import datetime
import sqlite3
from flask import g
DATABASE = '..\Project\oop-group-3\database'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

class Journal:
    def __init__(self):
        self.__time = datetime.now
        self.__log = {}

    def log_meal(self, meal):
        index = 0
        self.__log[index] = meal + "" + str(datetime.now)
        print(self.__log)

day = Journal()
day.log_meal('Chicken rice')
