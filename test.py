import datetime
import sqlite3

def get_current_time(): #function to get the current date&time stamp without microseconds
    return datetime.datetime.now().replace(microsecond=0)

def date_input_validate():
    while True:
        input_date = input("""\nType in 'today' if you want to see the statistics for today or enter the date in YYYY-MM-DD format: """).lower()
        if input_date == 'today':
            return 'today'
        else:
            try:
                return datetime.datetime.strptime(input_date, '%Y-%m-%d')
            except ValueError:
                print("Incorrect date format!")

def total_time(input_date):
    if input_date == 'today':
        time_period = get_current_time().strftime('%Y-%m-%d')
    else:
        time_period = datetime.datetime.strftime(input_date, '%Y-%m-%d')
    with sqlite3.connect('clocker.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT log_type, time FROM logs
        WHERE date = (?) ORDER BY datetime""", (time_period,))
        all_logs_per_date = cursor.fetchall()
        if not all_logs_per_date:
            print(f"\nNo logs found for {time_period}\n")
            return
        total_focus = datetime.timedelta()
        for log in all_logs_per_date:
            log_time = datetime.datetime.strptime(log[1], '%H:%M:%S')
            if log[0] == 'in':
                clock_in_time = log_time
            elif log[0] == 'out':
                total_focus += log_time - clock_in_time
        hours, remainder = divmod(total_focus.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f'\nTotal focus time for: {time_period} is {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds \n')


while True:
    decision = input(""">>STATISTICS<<
    d:  total focus time for a given date
    w:  total focus time for a given week
    m:  total focus time for a given month
Type the shortcut for the event: """).lower()
    if decision == 'd':
        total_time(date_input_validate())
    



#chat gave an idea for improvement: 3. Variable Initialization - fine but possibly need a different approach - combine it with calculating midnight