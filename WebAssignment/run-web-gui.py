#!/usr/bin/python
import sqlite3 as sql
from datetime import datetime
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('home.html')

@app.route('/list', methods=['POST'])
def display():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        print start
        startObj = datetime.strptime(start, '%Y-%m-%d')
        endObj = datetime.strptime(end, '%Y-%m-%d')

        s = startObj.strftime('%m/%d/%Y')
        e = endObj.strftime('%m/%d/%Y')

        con = sql.connect("/home/pi/ELSpring2018/WebAssignment/myTemps.db")
        cur = con.cursor()
        con.row_factory = sql.Row

        cur.execute('''SELECT * FROM myTemps WHERE currentTime BETWEEN ? AND ?''', (s, e,))

        rows = cur.fetchall();
        return render_template('list.html',rows = rows)
    con.close()

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)

