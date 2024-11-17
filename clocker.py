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

def sprint_mode():
    while True:
        decision = input(""">>SPRINT MODE<<
        i:          Clocking in
        o:          Clocking out
        back:       Back to the previous menu
    Type the shortcut for the event: """).lower()
        if decision in ('i', 'o'):
            comment = input("Comment: ")
            save_log(decision, comment)
        elif decision == 'back':
            print('')
            break
        else:
            print('Invalid option\n')
         
def slow_mode():
    while True:
        decision = input(""">>SLOW MODE<<
        i:          Clocking in
        o:          Clocking out
        back:       Back to the previous menu
    Type the shortcut for the event: """).lower()
        if decision in ('i', 'o'):
            comment = input("Comment: ")
            save_log(decision, comment)
        elif decision == 'back':
            print('')
            break
        else:
            print('Invalid option\n')

def statistics():
    pass

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
    mode = input(""" Choose mode:
    sprint:     25min focus and 5 min break. When intensive focus is needed
    slow:       1h15min focus and 15min break. For doing practice tasks
    statistics: Shows total focus time for a given day / week / month / year
    logs:       Browse through logs
    showlast:   Displays last log
    removelast: Removes last log
    exit:       Closes the program
Type the shortcut for the event: """).lower()
    modes = {
        'sprint': sprint_mode, 
        'slow': slow_mode, 
        'statistics': statistics, 
        'logs': logs_menu, 
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