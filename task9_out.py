import sqlite3
import csv
from datetime import datetime, timedelta
from math import ceil
import sys

input_date = sys.argv[1]

# Validate input
try:
    datetime.strptime(input_date, "%Y%m%d")
except ValueError:
    raise ValueError("Incorrect date format, should be YYYYMMDD")

# Convert the input date into a datetime form that can be manipulated
input_dt = datetime.strptime(input_date, "%Y%m%d")  # datetime object
comp_date = input_dt.strftime("%Y/%m/%d, %H:%M:%S")  # str object
comp_dt = datetime.strptime(comp_date, "%Y/%m/%d, %H:%M:%S")  # datetime object

# Determine the bounds for day, week and month based off the input date
# Upper Bound for the day entered
day1 = timedelta(1)
comp_dt_1day = comp_dt + day1

# Lower Bound for the week ending on the day entered
week1 = timedelta(7)
comp_dt_1week = comp_dt - week1

# Calculating the month to check
# Check leap year
if int(input_date[:4]) % 4 == 0:
    # Check date 29,30,31
    if input_date[4:] in ['0329', '0330', '0331']:
        comp_dt_1month = datetime.strptime(input_date[:4] + '0301', "%Y%m%d")
    # Check month - March
    elif input_date[4:6] == '03':
        month1 = timedelta(28)
        comp_dt_1month = comp_dt - month1
    else:
        month1 = timedelta(30)
        comp_dt_1month = comp_dt - month1
# Non-leap year
else:
    # Check date 28,29,30,31
    if input_date[4:] in ['0328', '0329', '0330', '0331']:
        comp_dt_1month = datetime.strptime(input_date[:4] + '0301', "%Y%m%d")
    # Check month - March
    elif input_date[4:6] == '03':
        month1 = timedelta(27)
        comp_dt_1month = comp_dt - month1
    else:
        month1 = timedelta(30)
        comp_dt_1month = comp_dt - month1

connect = sqlite3.connect('task9.db')  # Edit this line if you want the summary for another database
cursor = connect.cursor()

users = cursor.execute("SELECT username FROM users").fetchall()
users_with_sesh = cursor.execute("SELECT username FROM sessions").fetchall()
user_list = []

for (user,) in users_with_sesh:
    if user not in user_list:
        user_list.append(user)

data = []
for (user,) in users:  # Using the list of users from the users table will give the output the same order
    if user in user_list:  # Using user_list will only give the users with sessions

        query = "SELECT start,end FROM sessions WHERE username = ? AND start >= ? AND end < ? "
        args = (user, str(comp_date), str(comp_dt_1day.strftime("%Y/%m/%d, %H:%M:%S")))
        sessions_day = cursor.execute(query, args).fetchall()

        # On the day
        day_tot = 0
        for (a, b) in sessions_day:
            time = datetime.strptime(b, "%Y/%m/%d, %H:%M:%S") - datetime.strptime(a, "%Y/%m/%d, %H:%M:%S")
            day_tot += ceil(time.seconds / 3600 * 10) / 10

        # Over the previous week
        query = "SELECT start,end FROM sessions WHERE username = ? AND start >= ? AND end < ? "
        args = (user, str(comp_dt_1week.strftime("%Y/%m/%d, %H:%M:%S")), str(comp_dt_1day.strftime("%Y/%m/%d, %H:%M:%S")))
        sessions_week = cursor.execute(query, args).fetchall()

        week_tot = 0
        for (a, b) in sessions_week:
            time = datetime.strptime(b, "%Y/%m/%d, %H:%M:%S") - datetime.strptime(a, "%Y/%m/%d, %H:%M:%S")
            week_tot += ceil(time.seconds / 3600 * 10) / 10

        # Over the previous month
        query = "SELECT start,end FROM sessions WHERE username = ? AND start >= ? AND end < ? "
        args = (user, str(comp_dt_1month.strftime("%Y/%m/%d, %H:%M:%S")), str(comp_dt_1day.strftime("%Y/%m/%d, %H:%M:%S")))
        sessions_month = cursor.execute(query, args).fetchall()

        month_tot = 0
        for (a, b) in sessions_month:
            time = datetime.strptime(b, "%Y/%m/%d, %H:%M:%S") - datetime.strptime(a, "%Y/%m/%d, %H:%M:%S")
            month_tot += ceil(time.seconds / 3600 * 10) / 10

        data.append([user, day_tot, week_tot, month_tot])

connect.close()

with open('task9_out.csv', 'w', newline='') as out:
    csv_out = csv.writer(out)
    csv_out.writerows(data)
