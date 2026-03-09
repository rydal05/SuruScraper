from flask import Flask

app = Flask(__name__)
@app.route("/")
def index():
    return "index page"

@app.route("/history")
def history():
    return "history page"