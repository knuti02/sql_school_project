import sqlite3

# class for togrute
from util import *

con = sqlite3.connect("jernbane.db")

cursor = con.cursor()
cursor.execute("SELECT * FROM sqlite_master")


def addKundeordre(cursor, ordrenummer, dato_for_kjøp, tid, kundenummer, dato_for_tur, rute_id):
    cursor.execute(
        '''
        INSERT INTO Kundeordre (
            ordrenummer, dato_for_kjøp, tid, kundenummer, dato_for_tur, rute_id)
        VALUES (
            ?, ?, ?, ?, ?, ?
        )      

        ''', (ordrenummer, dato_for_kjøp, tid, kundenummer, dato_for_tur, rute_id)
    )

    con.commit()


def addBillett(cursor, Billett_ID, Plass_nr, StartStasjon_ID, SluttStasjon_ID, ordrenummer, Vogn_ID, Billettype, Indeks):
    cursor.execute(
        '''
        INSERT INTO Billett (
            Billett_ID, Plass_nr, StartStasjon_ID, SluttStasjon_ID, ordrenummer, Vogn_ID, Billettype, Indeks)
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?
        ) 
        ''', (Billett_ID, Plass_nr, StartStasjon_ID, SluttStasjon_ID, ordrenummer, Vogn_ID, Billettype, Indeks)

    )
    con.commit()


# addKundeordre(cursor, 7, "26/03/23", "12:00", 1, "03/04/23", 2)
addBillett(cursor, 8, 2, 1, 2, 7, 2, "Sovebillett", 2)


con.close()
