#!/usr/bin/env python
import sqlite3
import time
import datetime
from flask import Flask, render_template, Response, url_for, request
import picamera
import RPi.GPIO as GPIO
app = Flask(__name__)

@app.route("/<p>/<a>")
def moveServo(p, a):
    GPIO.setmode(GPIO.BOARD)
    pin = int(p)
    GPIO.setup(pin,GPIO.OUT)
    pwm=GPIO.PWM(pin,50)
    pwm.start(0)

    # formula to determine proper duty cycle
    angle = int(a)
    dc = 1/18*(angle)+2
    GPIO.output(pin,True)
    pwm.ChangeDutyCycle(12)
    time.sleep(1)
    GPIO.output(pin,False)
    #pwm.ChangeDutyCycle(0)
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

