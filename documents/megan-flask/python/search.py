from flask import *
from wtforms import StringField
import re


def Search(): 
    search = request.form("search")
    result = re.fullmatch(r'\w', search, flags=0)


