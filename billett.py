import sqlite3
from util import *
from togrute import start_to_finish

cursor = create_connection()[1]

class Billett:
    def __init__(self, billett_id, plass_nr, start_stasjon, slutt_stasjon, ordrenummer, vogn_id, billettype):
        self.billett_id = billett_id
        self.plass_nr = plass_nr
        self.start_stasjon = start_stasjon
        self.slutt_stasjon = slutt_stasjon
        self.ordrenummer = ordrenummer
        self.vogn_id = vogn_id
        self.billettype = billettype


def makeOrder(kundenummer, dato):
    try:
        cursor.execute(
            '''SELECT MAX(Billett_ID) FROM Billett''')
        
        next_order = cursor.fetchone()[0]
    except:
        next_order = -1

    cursor.execute(
        '''
        INSERT INTO Kundeordre VALUES (?,?,?,?)
        ''', (next_order + 1, getDateNow(), getTimeNow(), kundenummer)
    )


def orderTickets(kundenummer, dato, start_stasjon, slutt_stasjon):
    tickets = []
    available_tickets=[]
    number_of_tickets = input("Hvor mange billetter vil du kjøpe?\n")
    i = 0
    
    info = {
        "plass_nr" : [],
        "vogn_id" : [],
        "billettype" : [] 
    }
    
    while i < int(number_of_tickets):
        plass_nr = int(input("Hvilket plassnummer?\n"))
        vogn_id = int(input("Hvilken vogn?\n"))
        billettype = input("Hvilken billettype?\n")
        
        
        
        info["plass_nr"].append(plass_nr)
        info["vogn_id"].append(vogn_id)
        info["billettype"].append(billettype)
        i += 1
    
    makeOrder(kundenummer, dato)
    cursor.execute(
            '''SELECT MAX(ordrenummer) FROM Kundreordre''')
    ordrenummer = cursor.fetchone()[0]
    
    for i in range(len(info["plass_nr"])):
        ticket = makeTicket(info["plass_nr"][i], start_stasjon, slutt_stasjon, ordrenummer, info["vogn_id"][i], info["billettype"][i])
        tickets.append(ticket)
    
    insertTicketsToDatabase(tickets)
        

def makeTicket(plass_nr, start_stasjon, slutt_stasjon, ordrenummer, vogn_id, billettype):
    try:
        cursor.execute(
            '''SELECT MAX(Billett_ID) FROM Billett''')
        
        max_value = cursor.fetchone()[0]
    except:
        max_value = -1
    
    return Billett(max_value + 1, plass_nr, start_stasjon, slutt_stasjon, ordrenummer, vogn_id, billettype)


def find_legal_tickets(dato, tid, start_stasjon, slutt_stasjon):
    info_today = start_to_finish(cursor, start_stasjon, slutt_stasjon, getWeekdayBasedOnDate(dato), tid)
    info_tomorrow = start_to_finish(cursor, start_stasjon, slutt_stasjon, getNextDay(getWeekdayBasedOnDate(dato)), "00:00")
    routes = []
    
    for i in info_today:
        routes.append((i[0], dato, i[1], i[2]))
    for i in info_tomorrow:
        routes.append((i[0], nextDate(dato), i[1], i[2]))   
     
    # Spør bruker hvilken av rutene hen vil velge
    for i in range(len(routes)):
        print(f"Forslag {i}: rute {routes[i][0]}, dato: {routes[i][1]}, avgangstid: {routes[i][2]}, ankomsttid: {routes[i][3]}")
        
    choice = int(input("Hvilket forslag (nummer) vil du ha?:\n"))
    choice = routes[choice]
    
    cursor.execute(
        '''
        SELECT
            

        FROM
            Togrute
            JOIN
            Kundeordre
            WHERE
                Togrute.rute_ID = Kundeordre.rute_id
        WHERE
            rute_id = ?
            AND
            dato_for_tur = ?
        ''', (choice[0], choice[1])
    )
    
    return True

    
def insertTicketsToDatabase(tickets):
    for ticket in tickets:
       cursor.execute(
        '''
        INSERT INTO Billett VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (ticket.billett_id, ticket.plass_nr, 
              ticket.start_stasjon, ticket.slutt_stasjon, 
              ticket.ordrenummer, ticket.vogn_id, 
              ticket.billettype)
        ) 