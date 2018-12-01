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
        self.__time = str(datetime.now().strftime("%d-%m-%y %H:%M:%S"))
        self.__log = {}

    def log_meal(self, meal):
        self.__log[self.__time] = meal
        print(self.__log)

day = Journal()
day.log_meal('Chicken rice')
