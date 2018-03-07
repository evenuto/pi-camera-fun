#!/usr/bin/python
import sqlite3 as sql
import os
import time
import datetime
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/list')
def list():
    con = sql.connect("/home/pi/ELSpring2018/WebAssignment/myTemps.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM myTemps")

    rows = cur.fetchall();
    return render_template("list.html",rows = rows)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
