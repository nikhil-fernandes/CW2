# CW2
Resources related to a CW project which required the setup of a database and various scripts to interact with it. The scripts either produce output files depending on the contents of the database or change the database depending on a input .csv file.

#### initDB.ipynb
Jupyter Notebook that initialises and creates a new database in a form to interact with the other scripts in this repo. This database stores user information (username, password), their previous sessions, currently active sessions, and details of vehicle traffic each user has recorded. This notebook uses SQLite3 to set up the local database.

#### task8_in.py
Python script designed to edit a database set up using initDB. The script uses a .csv file to add new traffic observations or edit existing entries in this table of the database.

#### task8_out.py
Python script that outputs a .csv file depending on the contents of a given database consistent with initDB. 
The output file details the traffic observations between two given time stamps, where the traffic observations are summarised by the vehicles seen at a particular location are listed according to the number of occupants in the vehicle.

#### task8_traffic_input.csv
An example .csv file that task8_in is designed to anticipate

#### task9_in.py
Python script designed to edit a database set up using initDB. The script inserts additional entries to the 'sessions' table of the database, according to an input .csv file.

#### task9_login_input.csv
An example .csv file that task9_in is designed to anticipate

#### task9_out.py
Python script that outputs a .csv file depending on the contents of a given database consistent with initDB. 
The output file details the total session time each user has recorded in the database based on an input date. The output file produces 3 values for each recorded user: total session time for the input date, for the week ending on the input date, and for the month ending on the input date. Session times are produced in hours.
