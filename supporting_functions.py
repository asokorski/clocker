import datetime
import sqlite3
import os
import atexit
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" #to disable a welcome message from pygame community
import pygame
from colorama import Fore, Style


#to make sure that no matter where the app is execute it will always use database in the same directory as the app:
app_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(app_dir, 'clocker.db') #makes sure path is correct in any OS


# To initaliaze the sound for timer and ensure it cleans up the memory whenever/however the program is closed:
sound_path = os.path.join(app_dir, 'bell.mp3')
pygame.mixer.init()
bell_sound = pygame.mixer.Sound(sound_path)
atexit.register(pygame.mixer.quit)


def get_current_time(): #function to get the current date&time stamp without microseconds
    return datetime.datetime.now().replace(microsecond=0)


#validation of year for input in week calculations and weekly logs display
def validate_year():
    while True:
        year = input("Enter year in YYYY format: ")
        try:
            year = datetime.datetime.strptime(year,'%Y')
            year_str = datetime.datetime.strftime(year, '%Y')
            return year_str
        except ValueError:
            print('Incorrect year!')


#to create a database in case there is no clocker.db database found in the app folder
def create_database():
    connection = sqlite3.connect(database_path)
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


#displaying the last 3 logs in main menu and sprint/slow modes. Marking the latest one
def last_three_logs():
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute("""
SELECT log_type, datetime, comment FROM logs ORDER BY datetime DESC LIMIT 3;
""")
        last_three_logs = cursor.fetchall()
    if len(last_three_logs) >= 3:
        third_one = last_three_logs[2]
        second_one = last_three_logs[1]
        if last_three_logs[0][0] == 'in':
            last_one = f'{Style.BRIGHT}{Fore.RED}{last_three_logs[0]}{Style.RESET_ALL}'
        elif last_three_logs[0][0] == 'out':
            last_one = f'{Style.BRIGHT}{Fore.GREEN}{last_three_logs[0]}{Style.RESET_ALL}'
        # last_one = last_three_logs[0]
        status = f"""Last 3 logs:
            {third_one}
            {second_one}
        >>> {last_one}<<<"""
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
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO logs (log_type, datetime, date, week_number, day_of_week, time, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?) """, (log_type, datetime_str, date_str, week_number, day_of_week, time_str, comment))
        connection.commit()
    print(f"Log: '{log_type} {date_str} week:{week_number} {day_of_week} {time_str} {comment}' saved!")