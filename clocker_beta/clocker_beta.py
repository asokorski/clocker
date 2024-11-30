# v.0.1.0 - basic functions - shortcuts for the events, reading and removing last log and closing program. Console based. Saving data as csv
# v.0.2.0 added week days names, removed different events; just clocking, remove, exit
# LATER: GUI, work with a database, converting to web app

import datetime
import csv
import time
import os

#to make sure that no matter where the program is executed it will always use the log in the same directory
script_dir = os.path.dirname(os.path.abspath(__file__)) #gets the directory of the program
log_path = os.path.join(script_dir, 'clocker_beta.csv') #concatenates the directory with log name ensuring that path is correct in every OS

def get_current_time(): #function to get the current date&time stamp without microseconds
    return datetime.datetime.now().replace(microsecond=0)

def write_to_csv(event, timestamp, comment): #function to save a log
    with open(log_path, 'a', newline='') as file:
        writer = csv.writer(file) #csv.writer is formatiing the values in the row into csv format
        date = timestamp.strftime('%Y-%m-%d')
        time = timestamp.strftime('%H:%M:%S')
        week_day = timestamp.strftime('%A')
        writer.writerow([event, timestamp, date, week_day, time, comment]) #writerow gets the values into one row
 
        print(f"Log: '{event} {timestamp} {week_day} {comment}' saved!\n") #to get the log displayed

def remove_log(): #opens the file in write mode, shows the last line, removes it and overrites the file with the modified version
    with open(log_path, 'r') as file:
        reader = list(csv.reader(file))
        if len(reader) == 1:
            print("There are no logs!")
        else:
            print("Do you want to remove log: ", str(reader[-1]), "?")
            remove_decision = input("yes/no: ").lower()
            if remove_decision == "yes":
                reader.pop()
                with open(log_path, 'w', newline='') as file:
                    writer = csv.writer(file) #csv.writer is formatiing the values in the row into csv format
                    writer.writerows(reader) #method 'writerows' overrites the file with the modified version
                print("Log removed successfully!\n")
            elif remove_decision == "no":
                print("Log not removed\n")
            else:
                print("Invalid option\n")

event_commands = {
"i": "Clocking in",
"o": "Clocking out"
}

exit_commands = ["exit", "quit"]
remove_commands = ["remove"]

while True:
    decision = input("""Clocking...
    i:      Clocking in
    o:      Clocking out
    exit:   Close the program
    remove: Displays last log asking to confirm removal
Type the shortcut for the event: """).lower()

    if decision in event_commands.keys():
        comment = input("Comment: ")
        write_to_csv(event_commands.get(decision), get_current_time(), comment) #getting value from event_commands, the date and the comment into csv
    elif decision in exit_commands:
        print("Closing the program...\n")
        time.sleep(1)
        break
    elif decision in remove_commands:
        remove_log()
    else:
        print("Invalid option\n")

