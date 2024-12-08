import datetime
import sqlite3
from colorama import Fore, Style
from stats_menu import date_input_validate
from supporting_functions import get_current_time, validate_year, database_path


#display logs menu, lets you decide which logs to display or/and add/remove log manually
def logs_menu():
    while True:
        mode = input(f"""\n{Style.BRIGHT}{Fore.YELLOW}>>>LOGS MENU<<<{Style.RESET_ALL}\n
        a:          Displays all logs
        d:          All logs for given day
        w:          All logs for given week
        m:          All logs for given month
        add:        Manually add a log
        rmv:        Pick and remove a log
        back:       Back to the main menu\n
Type the shortcut for the event: """).lower()
        if mode in ['a', 'd', 'w', 'm']:
            display_logs(mode)
        elif mode == 'add':
            add_log()
        elif mode == 'rmv':
            remove_log()
        elif mode == "back":
            print('Returning to main menu')
            break
        else:
            print("Incorrect input")


#function to display logs for a given period. Uses date_input_validate function
def display_logs(period):
    if period == 'a':
        filter = ''
    elif period == 'd':
        input_date = date_input_validate(period)
        if input_date == 'today':
            input_date = get_current_time().strftime('%Y-%m-%d')
        filter = f"WHERE date = '{input_date}'"
        print(f'Displaying all logs for: {input_date}')
    elif period == 'w':
        input_date = date_input_validate(period)
        year = validate_year()
        filter = f"""WHERE week_number = {input_date} AND strftime('%Y', datetime) = '{year}'"""
        print(f'Displaying all logs for week: {input_date} in {year}')
    elif period == 'm':
        input_date = date_input_validate(period)
        filter = f"WHERE date like '{input_date}%'"
        print(f'Displaying all logs for: {input_date}')

#universal connection for all time periods, gives back the logs
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        query = f"""SELECT * FROM logs {filter} ORDER BY datetime ASC"""
        cursor.execute(query)
        all_logs = cursor.fetchall()
        print(f"\n{'Index':<7} {'Log Type':<10} {'Datetime':<20} {'Date':<12} {'Week':<6} {'Day':<10} {'Time':<10} {'Comment':<20}")
        print('-' * 100)
        if not all_logs:
            print('No logs found for the entered time period')


        previous_log_type = None
        for log in all_logs:
            if log[1] == previous_log_type:
                print(f'{Style.BRIGHT}{Fore.RED}{log[0]:<7} {log[1]:<10} {log[2]:<20} {log[3]:<12} {log[4]:<6} {log[5]:<10} {log[6]:<10} {log[7]:20}{Style.RESET_ALL}')
            else:
                print(f'{log[0]:<7} {log[1]:<10} {log[2]:<20} {log[3]:<12} {log[4]:<6} {log[5]:<10} {log[6]:<10} {log[7]:20}')
                previous_log_type = log[1]


#function to add a log manually
def add_log(): #decision tree for adding a log
    decision = input('Do you want to manually add a log y/n? ').lower()
    if decision not in ['y', 'n']:
        print('Invalid decision!')
        return
    if decision == 'n':
        print('No logs added')
        return
    while True:
        log_type = input('Enter log type i/o: ')
        if log_type in ['in', 'out']:
            break
        elif log_type == 'i':
            log_type = 'in'
            break
        elif log_type == 'o':
            log_type = 'out'
            break
        else:
            print('Incorrect log type')

    while True: #entering and validating the date
        date = input('Enter date in YYYY-MM-DD: ')
        try:
            date_validate = datetime.datetime.strptime(date, '%Y-%m-%d')
            date_str = datetime.datetime.strftime(date_validate, '%Y-%m-%d')
            break
        except ValueError:
            print("Incorrect date format!")

    while True: #entering and validating the time
        time = input('Enter time in HH:MM:SS format: ')
        try:
            time_validate = datetime.datetime.strptime(time, '%H:%M:%S')
            time_str = datetime.datetime.strftime(time_validate, '%H:%M:%S')
            break
        except ValueError:
            print("Incorrect time format!")

    datetime_str = (f'{date_str} {time_str}') #combining date and time into datetime

    week_number = date_validate.isocalendar()[1] #getting week number from date

    day_of_week = date_validate.strftime('%A') #getting day name from date

    comment = input('Enter comment: ') #entering comment

    with sqlite3.connect(database_path) as connection: #combining all as one log into db
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO logs (log_type, datetime, date, week_number, day_of_week, time, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?) """, (log_type, datetime_str, date_str, week_number, day_of_week, time_str, comment))
        connection.commit()
        print(f"\nLog: '{log_type} {date_str} week:{week_number} {day_of_week} {time_str} {comment}' saved!")


#function to manually remove log with a given id
def remove_log():
    log_id = input('\nEnter id number of the log to remove or type "back": ')
    if log_id == 'back':
        return
    else:
        try:
            log_id = int(log_id)
        except ValueError:
            print("\nInvalid log id!")
            return

#connection to display the chosen log and remove it
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(("""SELECT * FROM logs WHERE id = ?"""), (log_id,))
        log_to_remove = cursor.fetchone()
        if not log_to_remove:
            print(f'\nThere are no logs with id: {log_id}')
            return
        decision = input(f'\nDo you want to remove log: {log_to_remove} | y/n ')
        if decision == 'n':
            print('No logs removed')
            return
        elif decision == 'y':
            cursor.execute(("""DELETE FROM logs WHERE id = ?"""), (log_id,))
            connection.commit()
            print('\nLog removed successfully!')
        else:
            print('\nInvalid decision!')