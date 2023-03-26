import sqlite3
from util import *

con = sqlite3.connect("jernbane.db")

cursor = con.cursor()
cursor.execute("SELECT * FROM sqlite_master")

class Billett:
    def __init__(self, billett_id, plass_nr, start_stasjon, slutt_stasjon, ordrenummer, vogn_id, billettype, indeks):
        self.billett_id = billett_id
        self.plass_nr = plass_nr
        self.start_stasjon = start_stasjon
        self.slutt_stasjon = slutt_stasjon
        self.ordrenummer = ordrenummer
        self.vogn_id = vogn_id
        self.billettype = billettype
        self.indeks = indeks

def viewOrders(kundenummer):
    cursor.execute(
        '''
          SELECT 
                o.ordrenummer,
                o.dato_for_tur,
                o.rute_id,
                b.Billettype,
                b.Indeks,
                b.Plass_nr,
                s1.navn AS start_stasjon,
                r1.ankomsttid_avgangstid AS avgangstid,
                s2.navn AS slutt_stasjon,
                r2.ankomsttid_avgangstid AS ankomsttid
            FROM 
                Kundeordre o
                JOIN Billett b ON o.ordrenummer = b.ordrenummer
                JOIN Stasjon_i_rute r1 ON b.StartStasjon_ID = r1.stasjon_ID AND o.rute_id = r1.rute_ID AND b.Indeks = r1.sekvensnummer
                JOIN Stasjon_i_rute r2 ON b.SluttStasjon_ID = r2.stasjon_ID AND o.rute_id = r2.rute_ID AND r1.sekvensnummer < r2.sekvensnummer
                JOIN Stasjon s1 ON b.StartStasjon_ID = s1.stasjon_ID
                JOIN Stasjon s2 ON b.SluttStasjon_ID = s2.stasjon_ID

            WHERE
                kundenummer = ?

        ''', (kundenummer,)
    )

    returnedInfo = cursor.fetchall()

    infoToReturn = []
    
    print("Dine billetter:\n")

    for i in returnedInfo:
        infoToReturn.append(i)
        print(
            f"Ordrenummer: {i[0]}, Dato for tur: {i[1]}, Rute ID: {i[2]}, Billettype: {i[3]}, Vognnummer: {i[4]}, Plass: {i[5]}, Avgangsstasjon {i[6]}, Avgangstid: {i[7]}, Ankomststasjon: {i[8]}, Ankomsttid: {i[9]}")

    return infoToReturn

    
viewOrders(1)


con.close()