import datetime
import sqlite3
import os
from stats import total_time, date_input_validate
from logs_menu import logs_menu

def create_database():
    connection = sqlite3.connect('clocker.db')
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_type TEXT NOT NULL,
    datetime DATETIME NOT NULL,
    date DATE NOT NULL,
    week_number INTEGER NOT NULL,
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

def last_three_logs():
    with sqlite3.connect('clocker.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
SELECT log_type, datetime, comment FROM logs ORDER BY datetime DESC LIMIT 3;
""")
        last_three_logs = cursor.fetchall()
    if len(last_three_logs) >= 3:
        third_one = last_three_logs[2]
        second_one = last_three_logs[1]
        last_one = last_three_logs[0]
        status = f"""Last 3 logs:
            {third_one}
            {second_one}
        >>> {last_one} <<<"""
        return status
    else:
        return ''

#getting dates and time from get_current_time() function 
#with .date(), time() methods to get only date or time in right data type and .strftime('%A') to get week day name in str data type
#converting all the data to strings before storing as sqlite would convert it anyway, better do it here to make sure nothing gets mess up
def save_log(log_type, comment):
    datetime_str = get_current_time().strftime('%Y-%m-%d %H:%M:%S')
    date_str = get_current_time().date().strftime('%Y-%m-%d')
    week_number = get_current_time().date().isocalendar()[1]
    day_of_week = get_current_time().strftime('%A')
    time_str = get_current_time().time().strftime('%H:%M:%S')
    with sqlite3.connect('clocker.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO logs (log_type, datetime, date, week_number, day_of_week, time, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?) """, (log_type, datetime_str, date_str, week_number, day_of_week, time_str, comment))
        connection.commit()
    print(f"Log: '{log_type} {date_str} week:{week_number} {day_of_week} {time_str} {comment}' saved!")

def sprint_mode(): #counter and bell sound to be added, possibly to be merged with slowmode
    while True:
        print('\n>>SPRINT MODE<<')
        print(last_three_logs())
        decision = input("""
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
            print('\nReturning to main menu')
            break
        else:
            print('Invalid option\n')
         
def slow_mode(): #counter and bell sound to be added, possibly to be merged with sprintmode
    while True:
        print('\n>>SLOW MODE<<')
        print(last_three_logs())
        decision = input("""
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
            print('\nReturning to main menu')
            break
        else:
            print('Invalid option\n')

def statistics():
    while True:
        decision = input("""\n>>STATISTICS<<
        d:      Total focus time for a given date
        w:      Total focus time for a given week
        m:      Total focus time for a given month
        back:   Back to the previous menu\n
Type the shortcut for the event: """).lower()
        if decision in ['d', 'w', 'm']:
            total_time(date_input_validate(decision))
        elif decision == 'back':
            print('\nReturning to main menu')
            return            
        else:
            print("\nInvalid option")

def remove_last_log():
    while True:
        with sqlite3.connect('clocker.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT log_type, datetime, day_of_week, comment FROM logs ORDER BY datetime DESC LIMIT 1;""")
            last_log = cursor.fetchone()
        if not last_log:
            print('\nNo logs to remove')
            break
        else:
            print('\n>>REMOVE LAST LOG<<')
            print(f'Last log: {last_log}')
            remove_decision = input('Do you want to remove the last log y/n? ').lower()
            if remove_decision == 'y':
                with sqlite3.connect('clocker.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute("""DELETE FROM logs WHERE datetime = (SELECT MAX(datetime) FROM logs);""")
                    connection.commit()
                print(f'Log {last_log} removed!')
                break
            elif remove_decision == 'n':
                print('No logs removed')
                break
            else:
                print('Invalid option\n')


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
    print("\n>>MAIN MENU<<")
    print(f'Current week: {get_current_time().date().isocalendar()[1]}')
    print(last_three_logs())
    mode = input("""\nChoose mode:
    s:          Sprint. 25min focus and 5 min break. When intensive focus is needed
    l:          Slow. 1h15min focus and 15min break. For doing practice tasks
    stat:       Statistics. Shows total focus time for a given day / week / month
    log:        Browse through logs, manually add or remove
    rl:         Remove last log
    exit:       Closes the program \n
Type the shortcut for the event: """).lower()
    modes = {
        's':    sprint_mode, 
        'l':    slow_mode, 
        'stat': statistics, 
        'log':  logs_menu, 
        'rl':   remove_last_log}
    if mode in modes:
        modes[mode]()
    elif mode == "exit":
        exit(0)
    else:
        print("Incorrect input")
