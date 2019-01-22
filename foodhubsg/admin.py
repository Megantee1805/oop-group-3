from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite://// {_____}' {#location of database}

# Set the secret key to some random bytes. Use the command $ python -c 'import os; print(os.urandom(16))'
app.config['SECRET_KEY'] = 'mysecret'

#Initialize the db connection
db = SQLAlchemy(app)

admin = Admin(app)


#User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Coloumn(db.String(30))
    height = db.Coloumn(db.Float(5))
    weight = db.Coloumn(db.Float(5))
    email = db.Coloumn(db.Float(30))
    
admin.add_view(ModelView(User, db.session))    


class Food_Codes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Coloumn(db.String(20))
    code = db.Coloumn(db.Interger(10))
    calories = db.Coloumn(db.Interger(10))
    date_added = db.Coloumn(db.String(20))
    
    
admin.add_view(ModelView(Food_Codes, db.session))    
    
    
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Coloumn(db.String(20))
    location = db.Coloumn(db.String(20))
    ratings = db.Coloumn(db.String(20))
    
admin.add_view(ModelView(Vendor, db.session))    
    
    
class Vendor_Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Coloumn(db.String(20))
    code = db.Coloumn(db.Interger(10))
    calories = db.Coloumn(db.Interger(10))
    
admin.add_view(ModelView(Vendor_Items, db.session))    
        
        
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Coloumn(db.String(20))
    question = db.Coloumn(db.String(10000))
    answer = db.Coloumn(db.String(10000))
    
admin.add_view(ModelView(FAQ, db.session))    



        
        
if __name__ == '__main__':
    app.run(debug=True)
    
    
