#!/usr/bin/env python
import sqlite3
import time
import datetime
from flask import Flask, render_template, Response, url_for, request
import picamera 
import RPi.GPIO as GPIO
app = Flask(__name__)

@app.route("/moveServo")
def moveServo():
    GPIO.setmode(GPIO.BOARD)
    panPin = 11
    GPIO.setup(panPin,GPIO.OUT)
    pwm=GPIO.PWM(panPin,50)
    pwm.start(7)
    for i in range(0,180):
      DC=1./18.*(i)+2
      pwm.ChangeDutyCycle(DC)
    for i in range(0,180):
      DC=1/18.*i+2
      pwm.ChangeDutyCycle(DC)
    pwm.stop()
    GPIO.cleanup()
    return render_template('test.html')

@app.route("/", methods=['GET','POST'])
def main():
    return render_template('test.html')

@app.route("/takePic", methods=['GET','POST'])
def takePic():
    # connect to picture database
    try:
        db = sqlite3.connect('/home/pi/ELSpring2018/code/pics.db')
        cursor = db.cursor()
        currentTime=time.strftime('%x %X %Z') 

        # take new photo
        camera = picamera.PiCamera()
        timeTaken = time.strftime("%Y%m%d-%H%M%S")
        pic = camera.capture('static/'+timeTaken+'.jpg')
        camera.close()
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
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM pics''')
    rows = cursor.fetchall();
    db.close()
    return render_template('showPics.html',rows = rows)
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

# method to delete a desired picture from database/web interface
@app.route("/removePic/<path>", methods=['POST'])
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

    return render_template('showPics.html')

