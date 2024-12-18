import sqlite3
import datetime
import time
from colorama import Fore, Style
from supporting_functions import save_log, last_three_logs, database_path, bell_sound


#Setting up the right time and rings a bell when time ends up
def timer(mode_time, timer_type):
    try:
        while True:
            print((f"{Style.BRIGHT}{Fore.MAGENTA}\r{mode_time}{Style.RESET_ALL}"), end='', flush=True)
            time.sleep(1)
            mode_time -= datetime.timedelta(seconds=1)
            if mode_time < datetime.timedelta(seconds=0):
                bell_sound().wait_done()
                if timer_type == 's':
                    print(f'{Style.BRIGHT}{Fore.MAGENTA}\nEnd of sprint! Break time!{Style.RESET_ALL}')
                    break
                elif timer_type == 'l':
                    print(f'{Style.BRIGHT}{Fore.MAGENTA}\nEnd of slow! Break time!{Style.RESET_ALL}')
                    break
                elif timer_type == 'b':
                    print(f'{Style.BRIGHT}{Fore.MAGENTA}\nEnd of short break!{Style.RESET_ALL}')
                    break
                elif timer_type == 'bb':
                    print(f'{Style.BRIGHT}{Fore.MAGENTA}\nEnd of long break!{Style.RESET_ALL}')
                    break
    except KeyboardInterrupt:
        print(f"{Style.BRIGHT}{Fore.MAGENTA}\nTimer stopped manually!{Style.RESET_ALL}")
        return


#The control panel for clocking
def clocking(mode):
    while True:
        if mode == 's':
            print(f"\n{Style.BRIGHT}{Fore.YELLOW}>>>SPRINT MODE<<<{Style.RESET_ALL}")
        elif mode == 'l':
            print(f"\n{Style.BRIGHT}{Fore.YELLOW}>>>SLOW MODE<<<{Style.RESET_ALL}")
        else:
            print("Incorrect clocking mode!")
            break

        print(last_three_logs())
        decision = input("""
        i:          Clocking in
        o:          Clocking out
        b:          Short break 5 min
        bb:         Long break 15 min
        back:       Back to the previous menu
Type the shortcut for the event: """).lower()
        if decision == 'i' and mode == 's':
            comment = input("Comment: ")
            save_log('in', comment)
            mode_time = datetime.timedelta(minutes=25)
            timer(mode_time, mode)
        elif decision == 'i' and mode == 'l':
            comment = input("Comment: ")
            save_log('in', comment)
            mode_time = datetime.timedelta(hours=1, minutes=25)
            timer(mode_time, mode)
        elif decision == 'o':
            comment = input("Comment: ")
            save_log('out', comment)
        elif decision == 'b':
            mode_time = datetime.timedelta(minutes=5)
            timer(mode_time, 'b')
        elif decision == 'bb':
            mode_time = datetime.timedelta(minutes=15)
            timer(mode_time, 'bb')
        elif decision == 'back':
            print('\nReturning to main menu')
            break
        else:
            print('Invalid option\n')


#qucikly checks last (datetime-wise) log and asks if user wants to remove it
def remove_last_log():
    while True:
        with sqlite3.connect(database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT log_type, datetime, day_of_week, comment FROM logs ORDER BY datetime DESC LIMIT 1;""")
            last_log = cursor.fetchone()
        if not last_log:
            print('\nNo logs to remove')
            break
        else:
            print(f"\n{Style.BRIGHT}{Fore.YELLOW}>>>REMOVE LAST LOG<<<{Style.RESET_ALL}")
            print(f'Last log: {last_log}')
            remove_decision = input('Do you want to remove the last log y/n? ').lower()
            if remove_decision == 'y':
                with sqlite3.connect(database_path) as connection:
                    cursor = connection.cursor()
                    cursor.execute("""DELETE FROM logs WHERE datetime = (SELECT MAX(datetime) FROM logs);""")
                    connection.commit()
                print(f'Log {last_log} removed!')
                break
            elif remove_decision == 'n':
                print('No logs removed')
                break
            else:
                print('Invalid option')