
import sqlite3

from util import create_connection, getWeekdays
from billett import Billett
        
class BillettKjøpSystem:
    def __init__(self):
        self.billetter = []

    def leggTilBilletter(self, rute_id, startStasjon, sluttStasjon, date, tid):
        billett = Billett(rute_id, startStasjon, sluttStasjon, date, tid)
        self.billetter.append(billett)

    def visBilletter(self):
        for billett in self.billetter:
            print(f"Du har kjøpt billett(er) til - rute {billett.rute_id} - fra {billett.startStasjon} til {billett.sluttStasjon} kl {billett.tid}, {billett.date}")


def add_ticket(cursor, rute_id, startStasjon, sluttStasjon, date):
    try:
        cursor.execute(
        # Check if there are enough tickets available for the requested route and time
        '''
        SELECT 
            rute_id, 
            ankomsttid_avgangstid, 
            Navn_på_dag
        FROM 
            billett
            NATURAL JOIN 
            stasjon_i_rute
            NATURAL JOIN 
            Ukedag
        
        WHERE rute_id = ?
        AND ankomsttid_avgangstid = ?
        AND ankomsttid_avgangstid = ?
        AND Navn_på_dag = ?
        ''' ,(rute_id, startStasjon, sluttStasjon, date)
        ) 
    except sqlite3.Error as e:
        print(e)
        return None

    info = cursor.fetchall()
    return info
    
if __name__ == '__main__':
    cursor = create_connection()[1]
    print(add_ticket(cursor, "1", "Steinkjer", "Trondheim", "12.12.12"))


#     # loop to add tickets
#     while True:
#         rute_id = input("Rute: ")
#         startStasjon = input("Fra: ")
#         sluttStasjon = input("Til: ")
#         date = input("Dato (DD.MM.YY): ")
#         tid = input("Tid (HH:MM): ")
        
#         billett_system.leggTilBilletter(rute_id, startStasjon, sluttStasjon, date, tid)

#         add_more_tickets = input("Add more tickets? (y/n): ")
#         if add_more_tickets.lower() == "n":
#             break   

#     # display tickets
#     billett_system.visBilletter()




        