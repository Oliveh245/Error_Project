from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def search():
    return render_template("search.html")

@app.route("/no-solution")
def no_solution():
    return render_template("no-solution.html")

@app.route("/solutions")
def solutions():
    return render_template("list.html")

@app.route("/solution")
def solution():
    return render_template("solution.html")