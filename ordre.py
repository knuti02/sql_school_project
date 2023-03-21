import sqlite3

con = sqlite3.connect("jernbane.db")
cursor = con.cursor()
cursor.execute("SELECT * FROM sqlite_master")

def insertIntoTableKundeordre(dag: str, tid: str, kundenummer: int):
    try:
        cursor.execute(
            '''SELECT MAX(ordrenummer) FROM Kundeordre''')
        
        max_value = cursor.fetchone()[0]
    except:
        max_value = -1
        
    cursor.execute(
        '''INSERT INTO Kundeordre VALUES (?, ?, ?, ?)''', 
        (max_value + 1, dag, tid, kundenummer)
    )
    
    con.commit()
    

con.close()