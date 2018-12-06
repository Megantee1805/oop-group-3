from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/homepage/<user>')
def homepage(user):
    return render_template("homepage/html")

@app.route('/stats/<user>')
def stats(user):
    return render_template("stats.html", user=user)

@app.route('/<user>')
def profile(user):
    userID = request.args.get("user", " ")
    return render_template("profile.html", user = userID)

@app.route('/search')
def search(search): 
    search = request.args.get("search", " ")
    return render_template("search.html",  search = search)

if __name__ == '__main__':
    app.run(debug=True)
