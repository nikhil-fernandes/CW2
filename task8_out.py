import sqlite3
import csv
from datetime import datetime
import sys


# Function to check the format of the dates provided
def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y/%m/%d, %H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY/MM/DD, hh:mm:ss")


# Assign the dates to variables
input_start = sys.argv[1]
input_end = sys.argv[2]

# Check the format of the given dates
validate(input_start)
validate(input_end)

connect = sqlite3.connect('task8.db')  # Edit this input if you want the summary of another database
cursor = connect.cursor()
query = "SELECT location, type, COUNT(CASE WHEN occ = 1 THEN 1 END), COUNT(CASE WHEN occ = 2 THEN 1 END), COUNT(CASE WHEN occ = 3 THEN 1 END), COUNT(CASE WHEN occ = 4 THEN 1 END) FROM traffic WHERE count = 1 AND time BETWEEN ? AND ? GROUP BY location, type"
args = (str(input_start), str(input_end))
breakdown = cursor.execute(query, args).fetchall()

with open('task8_out.csv', 'w', newline='') as out:
    csv_out = csv.writer(out)
    csv_out.writerows(breakdown)
