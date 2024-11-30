import sqlite3
from supporting_functions import save_log, last_three_logs, database_path


#sprint and slow mode kept separately for different features
def sprint_mode():
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


def slow_mode():
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
            print('\n>>REMOVE LAST LOG<<')
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