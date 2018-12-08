import sqlite3
from flask import *

class User():
    def __init__(self):
        self.__name = ''
        self.__email = ''
        self.__password = ''

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_password(self, password):
       self.__password = password

    def get_password(self):
        return self.__password


class Calculator:
    def __init__(self):
        self.__height = 0
        self.__weight = 0
        self.__Bmi:float = 0

    def enter_details(self, height:float, weight:int):
        self.__height = height
        self.__weight = weight
        self.__Bmi = weight / (height * height)
