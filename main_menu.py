import sqlite3
import os
from colorama import Fore, Style
from stats_menu import statistics
from logs_menu import logs_menu
from supporting_functions import create_database, get_current_time, last_three_logs, database_path, app_dir
from modes import clocking, remove_last_log

print('Clocker v1.0.0 dev Adrian Sokorski')

# First loop to check if the datbase exists, if not, asking to create. Also checks if connection to db works
while True:
    if not os.path.exists(database_path):
        decide_if_create = input("Database for logs doesn't exist in the program directory. Do you want to create a it? y/n: ").lower()
        if decide_if_create == 'n':
            print("Program cannot be executed due to missing logs database. Closing the program...\n")
            exit(1)
        elif decide_if_create == 'y':
            create_database()
        else: 
            print("Incorrect input")
            continue
    else:
        try:
            connection = sqlite3.connect(database_path)
            # print("Database connection successful!") #for debugging
            connection.close()
            break
        except sqlite3.Error as error_message:
            print("Failed to connect to database:", error_message)
            exit(1)


# Main menu with dictionary for main functions. Functions s, l and rl are stored in 'modes.py'. stat and log separately
while True:
    print(f"\n{Style.BRIGHT}{Fore.YELLOW}>>>MAIN MENU<<<{Style.RESET_ALL}")
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
    other_modes = {
        'stat': statistics, 
        'log':  logs_menu, 
        'rl':   remove_last_log}
    if mode in ['s', 'l']: #if 's' or 'l' then respective clocking mode
        clocking(mode)
    elif mode in ['stat', 'log', 'rl']: #if other modes then respective from dictionary
        other_modes[mode]()
    elif mode == "exit":
        exit(0)
    else:
        print("Incorrect input")
