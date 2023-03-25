import sqlite3
from datetime import datetime, timedelta

def create_connection():
    con = sqlite3.connect("jernbane.db")
    cursor = con.cursor()
    return con, cursor

def getWeekdays():
    weekdays = ["Mandag", "Tirsdag", "Onsdag",
            "Torsdag", "Fredag", "Lørdag", "Søndag"]
    
    return weekdays

def getNextDay(day):
    weekdays = getWeekdays()

    if weekdays.index(day) == 6:
        return weekdays[0]
    else:
        return weekdays[weekdays.index(day) + 1]


def getPreviousDay(day):
    weekdays = getWeekdays()

    if weekdays.index(day) == 0:
        return weekdays[6]
    else:
        return weekdays[weekdays.index(day) - 1]


def getWeekdayBasedOnDate(date: str):
    eng_to_nor = {
        "Monday": "Mandag",
        "Tuesday": "Tirsdag",
        "Wednesday": "Onsdag",
        "Thursday": "Torsdag",
        "Friday": "Fredag",
        "Saturday": "Lørdag",
        "Sunday": "Søndag"
    }
    
    date_obj = datetime.strptime(date, '%d/%m/%Y')
    weekday = date_obj.strftime('%A')
    
    return eng_to_nor[weekday]

def getDateNow():
    now = datetime.now()
    current_date = now.date()
    
    return current_date

def nextDate(date_string):
    date_format = '%d/%m/%y'
    date = datetime.strptime(date_string, date_format)
    next_date = date + timedelta(days=1)
    return next_date.strftime(date_format)

def getTimeNow():
    now = datetime.now()
    current_time = now.time()
    
    return current_time