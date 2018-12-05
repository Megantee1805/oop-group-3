import sqlite3
from flask import g
DATABASE = '..\Project\oop-group-3\database'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

class Calculator:
    def __init__(self):
        self.__height = 0
        self.__weight = 0
        self.__Bmi:float = 0

    def enter_details(self, height:float, weight:int):
        self.__height = height
        self.__weight = weight
        self.__Bmi = weight / (height * height)

