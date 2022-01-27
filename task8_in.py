import sqlite3
import csv
from datetime import datetime
import sys

file = sys.argv[1]

with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    connect = sqlite3.connect('task8.db')  # Edit this input if you want to edit another database
    cursor = connect.cursor()

    for row in csv_reader:
        # Adjust format of the time from csv file format
        date = datetime.strptime(row[0], "%Y%m%d%H%M")
        date_in = date.strftime("%Y/%m/%d, %H:%M:%S")

        if row[1] == 'add':
            # Assume all additions are made by the same user (let it be called 'task8in')
            to_insert = ('task8in', row[2], row[3], int(row[4]), date_in, 1)

            cursor.execute("INSERT INTO traffic (userid,location,type,occ,time,count) VALUES (?,?,?,?,?,?)", to_insert)
            connect.commit()

        elif row[1] == 'undo':
            query = "SELECT recordid FROM traffic WHERE time = ? AND location = ? AND type = ? AND occ = ? AND count =1"
            args = (str(date_in), str(row[2]), str(row[3]), row[4])
            rec_list = cursor.execute(query, args).fetchall()

            if len(rec_list) == 0:
                continue
            else:
                rec_to_undo = max(rec_list)
                cursor.execute("UPDATE traffic SET count = 0 WHERE recordid = ?", (rec_to_undo[0],))
                connect.commit()

    connect.close()
    csv_file.close()
