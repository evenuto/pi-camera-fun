**Pi Camera Project**

HARDWARE Requirements:
- Raspberry pi 3
- Pi camera
- pan tilt servo motor setup

SOFTWARE
   1. Clone git repo
   2. run 'pip install -r requirements.txt' to get all requirements
   3. enable the pi camera
   4. Setup:
      - cd to your working project directory
      - create a folder called 'static' to hold the pictures
      - run 'createPicTable.py' (make sure to set the path to your database as your preferred location)
      - run 'takePic.py' to run website on localhost:8080 (again, make sure to edit path for database connection)
      - open your browser to localhost:8080 to view site
