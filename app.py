import sys
from flask import Flask, render_template,request,redirect
import sqlite3
# import scrape

app = Flask(__name__)

@app.route('/',methods =["GET", "POST"])
def index():
    # Fetch items from DB to display in browser
    conn = sqlite3.connect('suru.db')
    items = conn.execute("SELECT * FROM wishlist").fetchall()
    conn.close()
    if request.method == "POST":
        name = request.form.get("name")
        print(f"User submitted name: {name}")
        # handle route for handling submission
        pass # passover for now
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_link():
    url = request.form.get('url')
    # Logic to insert URL into SQLite
    return redirect('/')

if __name__ == "__main__":
    # scrape.init()
    app.run(host='0.0.0.0', port=5000)