**Pi Camera Project**

HARDWARE Requirements:
- Raspberry pi 3
- Pi camera
- pan tilt servo motor setup  
  ** In 'takePic.py', the pan servo is connected to GPIO pin 17, and the tilt servo is connected to GPIO pin 4. If you chose to use another set of pins, these values must be changed in 'takePic.py'.

SOFTWARE
   1. Clone git repo
   2. install all system and python requirements noted in requirements.txt
   3. enable the pi camera
   4. Setup:
      - cd to your working project directory
      - create a folder called 'static' to hold the pictures
      - run 'createPicTable.py' (make sure to set the path to your database as your preferred location)
      - run 'takePic.py' to run website on localhost:8080 (again, make sure to edit path for database connection)
      - open your browser to localhost:8080 to view site
