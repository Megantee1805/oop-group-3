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
    height = db.Coloumn(db.Numeric)
    weight = db.Coloumn(db.Numeric)
    email = db.Coloumn(db.Float(30))
    
    def __repr__(self):
        return '<User %r>' % (self.name)
    
admin.add_view(ModelView(User, db.session))    


class Food_Codes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Coloumn(db.String(20))
    code = db.Coloumn(db.String(10))
    calories = db.Coloumn(db.Integer(10))
    date_added = db.Coloumn(db.DateTime)
    
    def __repr__(self):
        return '<Food_Codes %r>' % (self.name)
    
admin.add_view(ModelView(Food_Codes, db.session))    
    
    
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Coloumn(db.String(20))
    location = db.Coloumn(db.String(20))
    ratings = db.Coloumn(db.Numeric)
    
    def __repr__(self):
        return '<Vendor %r>' % (self.restaurant_name)


#default setting for displaying tables and flask admin 
admin.add_view(ModelView(Vendor, db.session))    
    
#if default setting for displaying tables and flask admin doesnt work create customised version, add data to column that are part of primary key    
#class Vendor(ModelView):
#   form_columns = ["id", "restaurant_name", "location", "ratings"]
    
#Update   
#admin.add_view(SetView(Vendor, db.session))    
    
    
class Vendor_Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resturant_name = db.relationship('Vendor', backref="restaurant_name")
    code = db.Coloumn(db.String(10))
    calories = db.Coloumn(db.Interger(10))
    
    def __repr__(self):
        return '<vendor_Items %r>' % (self.name)
    
admin.add_view(ModelView(Vendor_Items, db.session))    
        
        
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Coloumn(db.String(20))
    question = db.Coloumn(db.Text)
    answer = db.Coloumn(db.Text)
    
    def __repr__(self):
        return '<FAQ %r>' % (self.name)
    
admin.add_view(ModelView(FAQ, db.session))    



        
        
if __name__ == '__main__':
    app.run(debug=True)
    
    
