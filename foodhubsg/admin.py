from flask import Flask, session, redirect, url_for, escape, request
from flask import Flask
from flask_admin import Admin
from flask import Flask, render_template
from flask_basicauth import BasicAuth
from flask_admin.contrib.sqla import ModelView




app = Flask(__name__)



# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app)
# Add administrative views here
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))


app.config['BASIC_AUTH_USERNAME'] = 'foodhubsg'
app.config['BASIC_AUTH_PASSWORD'] = 'amvz'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

# Set the secret key to some random bytes. Use the command $ python -c 'import os; print(os.urandom(16))'
app.secret_key = 

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
      
login_manager = LoginManager()
login_manager.init_app(app)
      
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
  
app.logger.error('An error occurred')





app.run()
