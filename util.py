import sqlite3

def create_connection():
    con = sqlite3.connect("jernbane.db")
    cursor = con.cursor()
    return con, cursor

def getWeekdays():
    weekdays = ["Mandag", "Tirsdag", "Onsdag",
            "Torsdag", "Fredag", "Lørdag", "Søndag"]
    
    return weekdays