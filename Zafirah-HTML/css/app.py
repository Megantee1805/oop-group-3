from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/')
def home():
    return render_template('static/mainpage.html')


if __name__ == '__main__':
    app.run()
