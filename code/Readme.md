**Pi Camera Project**

HARDWARE Requirements:
- Raspberry pi 3
- Pi camera
- pan tilt servo motor setup  
  ** As defined in 'app.py', the pan servo is connected to GPIO pin 17, and the tilt servo is connected to GPIO pin 4.
 If you chose to use another set of pins, these values must be changed in 'app.py'.

SOFTWARE
   1. Clone git repo
   2. install all system and python requirements noted in requirements.txt
   3. enable the pi camera
   4. Setup:
      - cd to your working project directory
      - create a folder called 'static' to hold the pictures that will be taken
      - in command prompt, run 'python3 createPicTable.py' (make sure to set the path to your database as your preferred location)
      - in command prompt, run 'python3 app.py' to host website on localhost:8080 (again, make sure to edit path for database connection)
      - open your browser to localhost:8080 to view site
