#!/usr/bin/env python
from importlib import import_module
import os
import sqlite3
import time
import datetime
from flask import Flask, render_template, Response, url_for
import picamera 

app = Flask(__name__)
 
@app.route("/", methods=['GET','POST'])
def main():
    return render_template('test.html')

@app.route("/takePic", methods=['GET','POST'])
def takePic():
    # connect to picture database
    try:
        db = sqlite3.connect('/home/pi/camApp/pics.db')
    except Error as e:
        print(e)
 
    cursor = db.cursor()
    currentTime=time.strftime('%x %X %Z') 

    # take new photo
    camera = picamera.PiCamera()
    pic = camera.capture('static/pic1.jpg')

    # store new photo in database
    cursor.execute('''INSERT INTO pics(picPath, datetime)
                  VALUES(?,?)''', (picPath, currentTime))
    db.commit()
    db.close()

    return render_template('test.html')

# method to display all pics taken so far
@app.route("/showPics", methods=['POST'])
def showPics():
    #if request.method == 'POST':
     #   try:
      #      db = sqlite3.connect('/home/pi/camApp/pics.db')
       # except Error as e:
        #    print(e)

      #  cursor = db.cursor()
       # db.row_factory = sql.Row
       # cur.execute('''SELECT * FROM pics''')

        # might need a different piece of code to render images...
       # rows = cur.fetchall();
       # return render_template('showPics.html',rows=rows)
    return render_template('showPics.html')

#    db.close()

 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
