# Time management and focus maintaining application


## Overview

Always having issues with time management I decided to create a tool that would help me organize proper time for studies or coding.
Users can log their sessions, view statistics, and manage logs through an intuitive terminal interface. Key features include SQLite database integration for persistent storage, colored terminal outputs for readability, and audio notifications for timer completions.


## Features

* ### Focus Modes:

    + Sprint Mode: 25 minutes of focus followed by a 5-minute break.

    + Slow Mode: 1 hour 15 minutes of focus followed by a 15-minute break.

* ### Log Management:

    + View, add, and delete logs.

    + Display the last three logs dynamically in the main menu.

* ### Statistics:

    + View total focus time for a specific day, week, or month.

    + Validate and calculate statistics for customizable time periods.


* Sound Notifications: Plays a notification sound when a timer ends.

* User-Friendly Interface: Intuitive menus with color-coded terminal output.


## Requirements

* Python 3.8 or later

* Required libraries:
    - `sqlite3` (built-in with Python)

    - `colorama`

    - `pygame`

* Supported Operating Systems: Linux, macOS, Windows


## Installation

1. Clone the repository:

`git clone https://github.com/your-repo/clocker.git`
`cd clocker`

2. Install dependencies:

`pip install -r requirements.txt`

3. Allow the program to create `clocker.db` on the first run.


## Running the Program

To start the application, execute:

`python3 main_menu.py`


## Usage

### Main Menu

The main menu offers the following options:

* Sprint Mode (s): Start a 25-minute focus timer.

* Slow Mode (l): Start a 1-hour 15-minute focus timer.

* Statistics (stat): View focus time statistics for day, week, or month.

* Log Management (log): Browse, add, or remove logs.

* Remove Last Log (rl): Deletes the most recent log entry.

* Exit: Close the application.


### Logs Menu

Manage logs with options to:

* View all logs or logs filtered by day, week, or month.

* Add a log manually.

* Remove a specific log by ID.


### Statistics

Displays total focus time for specific periods. Users can input the desired date, week, or month.


## Program Structure

* `main_menu.py`: Entry point for the application; manages the main menu.

* `modes.py`: Handles timer functionality and focus modes.

* `stats_menu.py`: Manages statistical calculations and display.

* `logs_menu.py`: Handles log management, including viewing and editing logs.

* `supporting_functions.py`: Utility functions for database management, time operations, and notifications.

* `clocker.db`: SQLite database file for storing logs.

* `bell.mp3`: The bell sound at the end of timer count.


## Planned Enhancements:

* Data export to CSV/Excel.

* GUI with graphical analytics

* Convert to web app
