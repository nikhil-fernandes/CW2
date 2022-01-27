import sqlite3
import csv
import sys
from datetime import datetime

input_file = sys.argv[1]

with open(input_file) as csv_file:  # use import sys; input_start = sys.argv[1] to take the file name as input
    csv_reader = csv.reader(csv_file, delimiter=',')

    rows_to_add = []
    for row in csv_reader:
        # Adjust format of the time from csv file format
        date = datetime.strptime(row[1], "%Y%m%d%H%M")
        date_in = date.strftime("%Y/%m/%d, %H:%M:%S")
        user = row[0]

        if row[2] == 'login':
            rows_to_add.append([user, date_in])

        if row[2] == 'logout':
            [row for row in rows_to_add if len(row) == 2 and row[0] == user][0].append(date_in)

    connect = sqlite3.connect('task9.db')  # Edit this line if you want to edit another database
    cursor = connect.cursor()
    for row in rows_to_add:
        query = "INSERT INTO sessions (username,start,end) VALUES (?,?,?)"
        arg = tuple(row)
        cursor.execute(query, arg)
        connect.commit()

    connect.close()
    csv_file.close()
