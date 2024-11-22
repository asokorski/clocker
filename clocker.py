import datetime
import sqlite3
import os

def create_database():
    connection = sqlite3.connect('clocker.db')
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_type TEXT NOT NULL,
    datetime DATETIME NOT NULL,
    date DATE NOT NULL,
    day_of_week TEXT NOT NULL,
    time TIME NOT NULL,
    comment TEXT);              
""")
    connection.commit()
    connection.close()
    print("Log database created! You can use the program now.")
    print('')

def get_current_time(): #function to get the current date&time stamp without microseconds
    return datetime.datetime.now().replace(microsecond=0)

#getting dates and time from get_current_time() function 
#with .date(), time() methods to get only date or time in right data type and .strftime('%A') to get week day name in str data type
#converting all the data to strings before storing as sqlite would convert it anyway, better do it here to make sure nothing gets mess up
def save_log(log_type, comment):
    datetime_str = get_current_time().strftime('%Y-%m-%d %H:%M:%S')
    date_str = get_current_time().date().strftime('%Y-%m-%d')
    day_of_week = get_current_time().strftime('%A')
    time_str = get_current_time().time().strftime('%H:%M:%S')
    with sqlite3.connect('clocker.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO logs (log_type, datetime, date, day_of_week, time, comment)
        VALUES (?, ?, ?, ?, ?, ?) """, (log_type, datetime_str, date_str, day_of_week, time_str, comment))
    print(f"Log: '{log_type} {date_str} {day_of_week} {time_str} {comment}' saved!\n")

def sprint_mode(): #counter and bell sound to be added, possibly to be merged with slowmode
    while True:
        decision = input(""">>SPRINT MODE<<
        i:          Clocking in
        o:          Clocking out
        back:       Back to the previous menu
    Type the shortcut for the event: """).lower()
        if decision == 'i':
            comment = input("Comment: ")
            save_log('in', comment)
        elif decision == 'o':
            comment = input("Comment: ")
            save_log('out', comment)
        elif decision == 'back':
            print('')
            break
        else:
            print('Invalid option\n')
         
def slow_mode(): #counter and bell sound to be added, possibly to be merged with sprintmode
    while True:
        decision = input(""">>SLOW MODE<<
        i:          Clocking in
        o:          Clocking out
        back:       Back to the previous menu
    Type the shortcut for the event: """).lower()
        if decision == 'i':
            comment = input("Comment: ")
            save_log('in', comment)
        elif decision == 'o':
            comment = input("Comment: ")
            save_log('out', comment)
        elif decision == 'back':
            print('')
            break
        else:
            print('Invalid option\n')

def statistics():
    while True:
        decision = input(""">>STATISTICS<<
        d:  total focus time for a given date
        w:  total focus time for a given week
        m:  total focus time for a given month
Type the shortcut for the event: """).lower()
        if decision == 'd':
            input_date = input("""\nType in 'today' if you want to see the statistics for today or enter the date in DD-MM-YYYY format: """)
            if input_date == 'today':
                today = get_current_time().strftime('%Y-%m-%d')
                with sqlite3.connect('clocker.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute("""SELECT log_type, time FROM logs
                    WHERE date = (?)""", (today,))
                    all_today = cursor.fetchall()
                    total_today = datetime.timedelta()
                    for log in all_today:
                        log_time = datetime.datetime.strptime(log[1], '%H:%M:%S')
                        if log[0] == 'in':
                            clock_in_time = log_time
                        elif log[0] == 'out':
                            total_today += log_time - clock_in_time
                    hours, remainder = divmod(total_today.total_seconds(), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    print(f'Total focus time for: {today} is {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds \n')

def logs_menu():
    pass

def show_last():
    pass

def remove_last_log():
    pass


# CORE LOGIC:
# First loop to check if the datbase exists, if not, asking to create. Also checks if connection to db works
while True:
    if not os.path.exists('clocker.db'): #os.path.exists returns True or False, so enough to say 'not' when we indicate that the condition is for False
        decide_if_create = input("Database for logs doesn't exist in the program directory. Do you want to create a it? y/n: ").lower()
        if decide_if_create == 'n':
            print("Program cannot be executed due to missing logs database. Closing the program...")
            exit(1)
        elif decide_if_create == 'y':
            create_database()
        else: 
            print("Incorrect input")
            continue
    else:
        try:
            connection = sqlite3.connect('clocker.db')
            # print("Database connection successful!") #for debugging
            connection.close()
            break
        except sqlite3.Error as error_message:
            print("Failed to connect to database:", error_message)
            exit(1)

# Main menu
while True:
    mode = input(""" \n Choose mode:
    s:          Sprint. 25min focus and 5 min break. When intensive focus is needed
    l:          Slow. 1h15min focus and 15min break. For doing practice tasks
    stat:       Statistics. Shows total focus time for a given day / week / month / year
    log:        Browse through logs
    showlast:   Displays last log
    removelast: Removes last log
    exit:       Closes the program \n
Type the shortcut for the event: """).lower()
    modes = {
        's': sprint_mode, 
        'l': slow_mode, 
        'stat': statistics, 
        'log': logs_menu, 
        'showlast': show_last, 
        'removelast': remove_last_log }
    if mode in modes:
        modes[mode]()
    elif mode == "exit":
        exit(0)
    else:
        print("Incorrect input")







#would be nide to open everything in a separate console since gonna use slow mode   
#two modes - sprint mode and slow mode
#logic that if it comes to midnight it will count the last sprint/slow from clock in up to midnight, and next from midnight to clockout
#other option - when the time is within the range of midnight, and let's say 6 hours after it, it will ask if should flag the entry for the previous day




# cursor.execute('SELECT * FROM logs')
# all_logs = cursor.fetchall()
# for log in all_logs:
#     print(log)

# INSERT INTO logs (log_type, datetime, date, day_of_week, time, comment)
# VALUES ('Clock In', '2024-11-15 08:00:00', '2024-11-15', 'Wednesday', '08:00:00', 'Focus session');
# DELETE FROM logs WHERE id = 1;
# INSERT INTO logs (log_type, datetime, date, day_of_week, time, comment)
# VALUES ('Clock Out', '2024-11-15 08:30:00', '2024-11-15', 'Wednesday', '08:30:00', 'Break started');