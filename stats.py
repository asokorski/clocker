import datetime
import sqlite3

def get_current_time(): #function to get the current date&time stamp without microseconds
    return datetime.datetime.now().replace(microsecond=0)

def date_input_validate(date_type): #making sure that the correct input was entered depending on the chosen mode
    while True:
        if date_type == 'd':
            input_date = input("""\nType in 'today' or enter the date in YYYY-MM-DD format: """).lower()
            if input_date == 'today':
                return 'today'
            else:
                try:
                    datetime.datetime.strptime(input_date, '%Y-%m-%d')
                    return input_date
                except ValueError:
                    print("\nIncorrect date format!")
        elif date_type == 'w':
            week_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
            input_date = input("""\nEnter the week number: """).lower()
            try:
                input_date = int(input_date)
                if int(input_date) in week_numbers:
                    return input_date
                else:
                    print('\nIncorrect week number!')
            except ValueError:
                print('\nIncorrect week number!')
        elif date_type == 'm':
            input_date = input("""\nEnter the date in YYYY-MM format: """).lower()
            try:
                datetime.datetime.strptime(input_date, '%Y-%m')
                return input_date
            except ValueError:
                print("\nIncorrect date format!")

def total_time(input_date):
    #deciding what is the mode for the calculation and how to input into query
    query_mode = ''
    if input_date == 'today':
        time_period = get_current_time().strftime('%Y-%m-%d')
        query_mode = 'day'
    else:
        time_period = input_date
        if len(str(input_date)) == 10:
            query_mode = 'day'
        elif len(str(input_date)) == 1 or len(str(input_date)) == 2:
            query_mode = 'week'
        elif len(str(input_date)) == 7:
            query_mode = 'month'

#total time calculating for 'today' or given day
    if query_mode == 'day':
        #both midnight times needed later for calculations when logs start with 'out' or ends with 'in'
        before_midnight = datetime.datetime.strptime('23:59:59', '%H:%M:%S')
        midnight = datetime.datetime.strptime('00:00:00', '%H:%M:%S')

#query execution for logs from a single day
        with sqlite3.connect('clocker.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT log_type, time FROM logs
            WHERE date like (?) ORDER BY datetime""", (time_period,))
            all_logs_per_date = cursor.fetchall()

            if not all_logs_per_date: #in case there are no logs
                print(f"\nNo logs found for {time_period}")
                return
            
            last_log = all_logs_per_date[-1]
            first_log = all_logs_per_date[0]
            total_focus = datetime.timedelta() #to initialize the variable as timedelta
            clock_in_time = None

            #main logic to go through fetched logs - same as for the other modes
            for log in all_logs_per_date:
                log_time = datetime.datetime.strptime(log[1], '%H:%M:%S')
                if log[0] == 'in':
                    clock_in_time = log_time
                elif log[0] == 'out' and clock_in_time:
                    total_focus += log_time - clock_in_time
                    clock_in_time = None

            #to count from midnight if first log is out and to midnight if last is in
            if (str(last_log[0])).strip().lower() == 'in':
                total_focus += before_midnight - clock_in_time
            if (str(first_log[0])).strip().lower() == 'out':
                total_focus +=  datetime.datetime.strptime(first_log[1], '%H:%M:%S') - midnight

#total time calculating for a given week
    elif query_mode == 'week':
        with sqlite3.connect('clocker.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT log_type, datetime FROM logs
            WHERE week_number = (?) ORDER BY datetime""", (time_period,))
            all_logs_per_date = cursor.fetchall()

            if not all_logs_per_date: #in case there are no logs
                print(f"\nNo logs found for week {time_period}")
                return
            
            total_focus = datetime.timedelta() #to initialize the variable as timedelta
            clock_in_time = None

            #main logic to go through fetched logs - same as for the other modes
            for log in all_logs_per_date:
                log_time = datetime.datetime.strptime(log[1], '%Y-%m-%d %H:%M:%S')
                if log[0] == 'in':
                    clock_in_time = log_time
                elif log[0] == 'out' and clock_in_time:
                    total_focus += log_time - clock_in_time
                    clock_in_time = None
     
            #both midnight times needed later for calculations when logs start with 'out' or ends with 'in'
            #condition for having the first fetched log as 'out' to sum up time from midnight that day  
            if all_logs_per_date[0][0].strip().lower() == 'out':
                first_date = all_logs_per_date[0][1].split(' ')[0]
                midnight = datetime.datetime.strptime(f"{first_date} 00:00:00", '%Y-%m-%d %H:%M:%S')
                total_focus += datetime.datetime.strptime(all_logs_per_date[0][1], '%Y-%m-%d %H:%M:%S') - midnight
            
            #to count up to midnight if last clocking is in
            if clock_in_time: 
                last_date = all_logs_per_date[-1][1].split(' ')[0]
                before_midnight = datetime.datetime.strptime(f"{last_date} 23:59:59", '%Y-%m-%d %H:%M:%S')
                total_focus += before_midnight - clock_in_time

            time_period = ("week " + time_period) #changing variable for the "Total focus time for (...)" display message

#total time calculating for the given month
    elif query_mode == 'month':
        with sqlite3.connect('clocker.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT log_type, datetime FROM logs
            WHERE date like (?) ORDER BY datetime""", ((time_period+'%'),))
            all_logs_per_date = cursor.fetchall()

            if not all_logs_per_date: #in case there are no logs
                print(f"\nNo logs found for {time_period}\n")
                return
            
            total_focus = datetime.timedelta() #to initialize the variable as timedelta
            clock_in_time = None

            #main logic to go through fetched logs - same as for the other modes
            for log in all_logs_per_date:
                log_time = datetime.datetime.strptime(log[1], '%Y-%m-%d %H:%M:%S')
                if log[0] == 'in':
                    clock_in_time = log_time
                elif log[0] == 'out' and clock_in_time:
                    total_focus += log_time - clock_in_time
                    clock_in_time = None
     
            #both midnight times needed later for calculations when logs start with 'out' or ends with 'in'
            #condition for having the first fetched log as 'out' to sum up time from midnight that day  
            if all_logs_per_date[0][0].strip().lower() == 'out':
                first_date = all_logs_per_date[0][1].split(' ')[0]
                midnight = datetime.datetime.strptime(f"{first_date} 00:00:00", '%Y-%m-%d %H:%M:%S')
                total_focus += datetime.datetime.strptime(all_logs_per_date[0][1], '%Y-%m-%d %H:%M:%S') - midnight
            
            #to count up to midnight if last clocking is in
            if clock_in_time: 
                last_date = all_logs_per_date[-1][1].split(' ')[0]
                before_midnight = datetime.datetime.strptime(f"{last_date} 23:59:59", '%Y-%m-%d %H:%M:%S')
                total_focus += before_midnight - clock_in_time

    #spliting the total time in hours, minutes, seconds
    hours, remainder = divmod(total_focus.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f'\nTotal focus time for {time_period} is {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds.')
