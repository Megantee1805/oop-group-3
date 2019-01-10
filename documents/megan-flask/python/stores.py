from flask import *
import sqlite3

class Stores:
    def __init__(self):
        self.__name = ''
        self.__menu_items:int = 0
        self.__code = ''
        self.__menu = {}

    def enter_menu(self, items):
        self.__menu = items
        for i in items:
            name = input('Name of item : ')
            calories = int(input('Calories of items '))
            self.__menu[name] = calories

    def set_code(self):
        code = input('Enter code number : ')
        code = code.isalnum()
        if code == True:
            print("Set successfully")
        else:
            print('Please try again')
            self.set_code()
