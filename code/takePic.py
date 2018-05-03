#!/usr/bin/env python
import os
import atexit
import sqlite3
import time
import datetime
from flask import Flask, render_template, Response, url_for, request
import picamera
import RPi.GPIO as GPIO

app = Flask(__name__)

global panServoAngle
global tiltServoAngle
panServoAngle = 90 #starting position for pan servo
tiltServoAngle = 90 #starting position for tilt servo
panPin = 17 #pin number for connecting pan servo to gpio board
tiltPin = 4 #pin number for connecting tilt servo to gpio board

#renders the main template for viewing
@app.route("/", methods=['GET','POST'])
def main():
    return render_template('test.html')

#move the servos
@app.route("/<servo>/<angle>")
def move(servo, angle):
        global panServoAngle
        global tiltServoAngle
        if servo == 'pan':
            if angle == '+':
                   panServoAngle = panServoAngle + 10
            else:
                panServoAngle = panServoAngle - 10
            os.system("python angleServo.py " + str(panPin) + " " + str(panServoAngle))
        if servo == 'tilt':
               if angle == '+':
                        tiltServoAngle = tiltServoAngle + 10
               else:
                    tiltServoAngle = tiltServoAngle - 10
               os.system("python angleServo.py " + str(tiltPin) + " " + str(tiltServoAngle))
        templateData = {
               'panServoAngle'   : panServoAngle,
               'tiltServoAngle'  : tiltServoAngle
        }
        return render_template('test.html', **templateData)


@app.route("/takePic", methods=['GET','POST'])
def takePic():
    # connect to picture database
    try:
        db = sqlite3.connect('/home/pi/ELSpring2018/code/pics.db')
        cursor = db.cursor()
        currentTime=time.strftime('%x %X %Z') 

        # take new photo
        camera = picamera.PiCamera() # uses the pi camera
        timeTaken = time.strftime("%Y%m%d-%H%M%S") # stores time pic is taken
        pic = camera.capture('static/'+timeTaken+'.jpg') # takes pic
        camera.close() # close camera connection
        picPath = timeTaken+".jpg"
        # store new photo in database
        cursor.execute('''INSERT INTO pics(picPath, datetime)
                  VALUES(?,?)''', (picPath, currentTime))
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return render_template('test.html')

# method to display all pics taken so far
@app.route("/showPics")
def showPics():
    db = sqlite3.connect('/home/pi/ELSpring2018/code/pics.db')
    db.row_factory = sqlite3.Row # creates rows for pics taken
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM pics''')
    rows = cursor.fetchall(); # fetches all rows of query result
    db.close()
    return render_template('showPics.html',rows = rows)

# method to delete a desired picture from database/web interface
@app.route("/showPics/<path>", methods=['GET','POST'])
def removePic(path):
    try:
        db = sqlite3.connect('/home/pi/ELSpring2018/code/pics.db')
        cursor = db.cursor()

        # delete the pic from database
        query = "DELETE FROM pics WHERE picPath LIKE '%s' " % path
        cursor.execute(query)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    db = sqlite3.connect('/home/pi/ELSpring2018/code/pics.db')
    db.row_factory = sqlite3.Row # creates rows for pics taken
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM pics''')
    rows = cursor.fetchall(); # fetches all rows of query result
    db.close()
    return render_template('showPics.html',rows = rows)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

