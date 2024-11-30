

#przekmin to ze przy wyswietlaniu logow z danego tygodnia i wyliczaniu total focusu z danego tygodnia trzeba jakos dodac z jakiego roku


#Invalid Dates: Try inputs like 2024-02-30.
#Empty Time: Leave the time input empty or use invalid formats like 99:99:99.
#Comment: Test with and without comments.
#Ambiguous Weeks: Test dates that fall in overlapping weeks at year boundaries (e.g., Dec 31 and Jan 1).

#IN STATS add the import from clocker py for get current time and remove it from stats
#actually try to remove from both

#then to make it to open in a separate console
#then work with the colors and sounds
#maybe to somehow make it print line by line so the user can catch what is changing in the console instead of printing all at once


import datetime


time = input('Enter time in HH:MM:SS format: ')

time_validate = datetime.datetime.strptime(time, '%H:%M:%S')
time_str = datetime.datetime.strftime(time_validate, '%H:%M:%S')

print(time_str)



# cursor.execute('SELECT * FROM logs')
# all_logs = cursor.fetchall()
# for log in all_logs:
#     print(log)

# INSERT INTO logs (log_type, datetime, date, day_of_week, time, comment)
# VALUES ('in', '2024-11-15 08:00:00', '2024-11-15', 'Wednesday', '08:00:00', 'Focus session');
# DELETE FROM logs WHERE id = 1;
# INSERT INTO logs (log_type, datetime, date, day_of_week, time, comment)
# VALUES ('out', '2024-11-15 08:30:00', '2024-11-15', 'Wednesday', '08:30:00', 'Break started');

#INSERT INTO logs (log_type, datetime, date, day_of_week, time, comment) VALUES ('in', '2024-11-22 23:50:00', '2024-11-22', 'Friday', '23:50:00', 'Midnight test')