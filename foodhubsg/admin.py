from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template
from flask_basicauth import BasicAuth
from flask import Flask, session, redirect, url_for, escape, request


app = Flask(__name__)

app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite://///tmp/test.db' #location of database

# Set the secret key to some random bytes. Use the command $ python -c 'import os; print(os.urandom(16))'
app.config['SECRET_KEY'] = 'mysecret'

#Initialize the db connection
db = SQLAlchemy(app)
    
admin = Admin(app)


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

#User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Coloumn(db.String(30))
    height = db.Coloumn(db.Numeric)
    weight = db.Coloumn(db.Numeric)
    email = db.Coloumn(db.String(30))
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    
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



app.config['BASIC_AUTH_USERNAME'] = 'foodhubsg'
app.config['BASIC_AUTH_PASSWORD'] = 'amvz'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

# Set the secret key to some random bytes. Use the command $ python -c 'import os; print(os.urandom(16))'
app.secret_key = 'this-is-totally-secret-guys-nobody-can-guess-this-trust-me'

@app.route('/secret')
@basic_auth.required
def secret_login_view():
    return render_template('login.html')

  
class MicroBlogModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
      
login_manager = LoginManager()
login_manager.init_app(app)
      
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
  
    
    
    
app.logger.error('An error occurred')



if __name__ == '__main__':
    app.run(debug=True)
    
    
