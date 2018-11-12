from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/homepage/<user>')
def homepage(user):
    return render_template("homepage.html", user=user)



if __name__ == '__main__':
    app.run(debug=True)

