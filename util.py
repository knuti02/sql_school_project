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
    
    date_obj = datetime.strptime(date, '%d/%m/%y')
    weekday = date_obj.strftime("%A")
    
    return eng_to_nor[weekday]

def getDateNow():
    now = datetime.now()
    current_date = now.date()
    
    return current_date

def nextDate(date: str):
    date_obj = datetime.strptime(date, '%d/%m/%y')
    next_date = date_obj + timedelta(days=1)
    return next_date.strftime('%A')

def getTimeNow():
    now = datetime.now()
    current_time = now.time()
    current_time = current_time.strftime("%H:%M")
        
    return current_time

if __name__ == "__main__":
    print(getTimeNow())