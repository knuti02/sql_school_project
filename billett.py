import sqlite3
from util import *
from togrute import start_to_finish, findIndex
from math import *

con, cursor = create_connection()

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
        
    def toString(self):
        print(self.billett_id, self.plass_nr, self.start_stasjon, self.slutt_stasjon, self.ordrenummer, self.vogn_id, self.billettype, self.indeks)


def makeOrder(kundenummer, dato, rute_id):
    try:
        cursor.execute(
            '''SELECT MAX(Billett_ID) FROM Billett''')
        
        next_order = cursor.fetchone()[0]
    except:
        next_order = -1

    cursor.execute(
        '''
        INSERT INTO Kundeordre VALUES (?, ?, ?, ?, ?, ?)
        ''', (next_order + 1, getDateNow(), getTimeNow(), kundenummer, dato, rute_id)
    )
    con.commit()


def orderTickets(kundenummer, dato, start_stasjon, slutt_stasjon):
    tickets = []
    info = {
        "id" : [],
        "plass_nr" : [],
        "indeks" : [],
        "billettype" : []
    }
    
    temp_list_of_sit = []
    temp_list_of_sleep = []
    
    tid = input("Når vil du dra?:\n")
    choice = findRoute(dato, tid, start_stasjon, slutt_stasjon)
    tickets = findLegalTickets(choice, start_stasjon, slutt_stasjon)
    
    print(f"Tilgjenglige billetter: {tickets}")

    number_of_tickets = int(input("Hvor mange billetter vil du kjøpe?\n"))    
    
    num = 0
    for i in tickets:
        for e in i:
            if isinstance(e, tuple):
                for element in e:
                    num += 1
            else:
                num += 1

    if number_of_tickets > num:
        print("Ikke nok billetter tilgjenglig!")
        return
    
    makeOrder(kundenummer, dato, choice[0])
    
    i = 0
    while i < int(number_of_tickets):
        indeks = int(input("Hvilken vogn?\n")) 
        id = getVognId(choice[0], indeks)
        type = getType(id)
        plass_nr = int(input("Hvilket plassnummer?\n"))
        
        if len(tickets[indeks -1]) == 12: 
            if plass_nr in temp_list_of_sit:
                print("Sete er ikke tilgjengelig!")
                continue
            
            temp_list_of_sit.append(plass_nr)
                
            if tickets[indeks - 1][plass_nr - 1] == 'X':
                print("Sete er ikke tilgjengelig!")
                continue
        else:
            if plass_nr in temp_list_of_sleep:
                print("Sete er ikke tilgjengelig!")
                continue
            
            temp_list_of_sleep.append(plass_nr)
            
            if 'X' in tickets[indeks - 1][floor(plass_nr / 2) + plass_nr % 2 - 1]:
                print("Sete er ikke tilgjengelig!")
                continue
        
        
        info["id"].append(id)
        info["plass_nr"].append(plass_nr)
        info["indeks"].append(indeks)
        info["billettype"].append(type)
        
        i += 1
        
    cursor.execute(
            '''SELECT MAX(ordrenummer) FROM Kundeordre''')
    ordrenummer = cursor.fetchone()[0]
    cursor.execute(
        '''SELECT stasjon_ID FROM Stasjon WHERE navn = ?''', (start_stasjon,))
    start_stasjon = cursor.fetchone()[0]
    cursor.execute(
        '''SELECT stasjon_ID FROM Stasjon WHERE navn = ?''', (slutt_stasjon,))
    slutt_stasjon = cursor.fetchone()[0]
    
    ordered_tickets = []
    for i in range(len(info["plass_nr"])):
        ticket = makeTicket(info["plass_nr"][i], start_stasjon, slutt_stasjon, ordrenummer, info["id"][i], info["billettype"][i], info["indeks"][i], i)
        ordered_tickets.append(ticket)
    
    insertTicketsToDatabase(ordered_tickets)
        

def makeTicket(plass_nr, start_stasjon, slutt_stasjon, ordrenummer, vogn_id, billettype, indeks, amount_made):
    try:
        cursor.execute(
            '''SELECT MAX(Billett_ID) FROM Billett''')
        
        max_value = cursor.fetchone()[0]
    except:
        max_value = -1
    
    return Billett(max_value + 1 + amount_made, plass_nr, start_stasjon, slutt_stasjon, ordrenummer, vogn_id, billettype, indeks)


def findRoute(dato, tid, start_stasjon, slutt_stasjon):
    info_today = start_to_finish(cursor, start_stasjon, slutt_stasjon, getWeekdayBasedOnDate(dato), tid)
    info_tomorrow = start_to_finish(cursor, start_stasjon, slutt_stasjon, nextDate(dato), "00:00")
    routes = []
    
    for i in info_today:
        routes.append((i[0], dato, i[1], i[2]))
    for i in info_tomorrow:
        routes.append((i[0], nextDate(dato), i[1], i[2]))
     
    # Spør bruker hvilken av rutene hen vil velge
    amount_of_routes = len(routes)
    for i in range(amount_of_routes):
        print(f"Forslag {i}: rute {routes[i][0]}, dato: {routes[i][1]}, avgangstid: {routes[i][2]}, ankomsttid: {routes[i][3]}")

    num = -1
    while not (num > 0 and num <= amount_of_routes):
        try:
            num = int(input("Hvilket forslag (nummer) vil du ha?:\n"))
        except:
            continue

    choice = routes[num] #(rute_id, dato, avgangstid, ankomsttid)
    
    
    
    return choice
    
def findLegalTickets(choice, startstasjon, sluttstasjon):
    wagons = getWagons(choice[0])
    tickets = findTikcetsByRouteOnDate(choice[0], choice[1])
    
    #for alle vogner, sjekk alle tickets assosiert med vognen, og se hvilke plasser som er tatt i en gitt strekning
    train = []

    start_index = findIndex(startstasjon, choice[0])
    slutt_index = findIndex(sluttstasjon, choice[0])
    for wagon in wagons:
        train.append([]) # legg til vogn i tog
        #gjør sjekk for sovevogn
        if wagon[3] == "Sovevogn":
            for i in range(0, wagon[2], 2):
                first_taken = False
                second_taken = False
                for ticket in tickets:
                    #ticket : (billett_id, billettype, plass_nr, vogn_id, indeks, navn_start, indeks_start, navn_slutt, indeks_slutt)
                    if i+1 == ticket[2] and wagon[1] == ticket[4]:
                        first_taken = True
                    if i+2 == ticket[2] and wagon[1] == ticket[4]:
                        second_taken = True
                
                tup = (i + 1, i + 2)
                
                if first_taken:
                    tup = ("X", i + 2)
                if second_taken:
                    tup = (i + 1, "X")
                if second_taken and first_taken:
                    tup = ("X", "X")
                
                train[-1].append(tup)
                
        else:
            for i in range(wagon[2]): # sjekk for hver plass om det finnes tickets med overlappende sekvensnummer-intervaller
                isTaken = False
                for ticket in tickets:
                    #ticket : (billett_id, billettype, plass_nr, vogn_id, indeks, navn_start, indeks_start, navn_slutt, indeks_slutt)
                    if max(start_index, ticket[6]) < min(slutt_index, ticket[8]) and i+1 == ticket[2] and wagon[1] == ticket[4]:
                        isTaken = True
                if isTaken:
                    train[-1].append("X")
                else:
                    train[-1].append(i+1)
            
    return train

def getWagons(rute_id):
    cursor.execute(
        '''
        SELECT
            Vogn_ID,
            `Index`,
            Antall_plasser,
            Vogntype

        FROM
            Togrute
            NATURAL JOIN
            InneholderVogn
            NATURAL JOIN 
            Vogn
                
        WHERE
            Togrute.rute_ID = ?
        ''', (rute_id,)
    )
    
    return cursor.fetchall() #(vogn_id, index, antall_plasser, vogntype)

    
#Finn alle tickets. Basert på tickets kan me se hvilke plasser som er tatt gitt en vogn.     
#Bruk dette til å finne ledige plasser i en vogn.

def findTikcetsByRouteOnDate(rute_id, dato):
    cursor.execute(
        '''
        SELECT
            Billett_ID,
            Billettype,
            Plass_nr,
            Vogn_ID,
            Indeks,
            StartStasjon.navn,
            sir_start.Sekvensnummer,
            SluttStasjon.navn,
            sir_slutt.Sekvensnummer

        FROM
            Billett
            NATURAL JOIN
            Kundeordre AS KO
            JOIN
            Stasjon AS StartStasjon
            JOIN 
            Stasjon AS SluttStasjon
            JOIN
            Stasjon_i_rute AS SIR_start
            JOIN
            Stasjon_i_rute AS SIR_slutt

        WHERE
            StartStasjon.stasjon_ID = StartStasjon_ID
            AND
            SluttStasjon.stasjon_ID = SluttStasjon_ID
            AND
            SIR_start.stasjon_ID = StartStasjon.stasjon_ID 
            AND
            SIR_slutt.stasjon_ID = SluttStasjon.stasjon_ID 
            AND
            SIR_start.rute_ID = KO.rute_id
            AND
            SIR_slutt.rute_ID = KO.rute_id
            AND
            KO.rute_id = ?
            AND
            dato_for_tur = ?
        ''', (rute_id, dato)
    )
    
    return cursor.fetchall() #(billett_id, billettype, plass_nr, vogn_id, indeks, navn_start, indeks_start, navn_slutt, indeks_slutt)


def getVognId(rute_id, indeks):
    cursor.execute(
        '''
        SELECT
            Vogn_ID
            
        FROM
            Togrute
            NATURAL JOIN
            Vognoppsett
            NATURAL JOIN
            InneholderVogn
        
        WHERE
            Togrute.rute_ID = ?
            AND
            InneholderVogn.'Index' = ?
        ''', (rute_id, indeks)
    )
    return cursor.fetchone()[0]

def getType(id):
    cursor.execute(
        '''
        SELECT
            Vogntype
            
        FROM
            Vogn
        
        WHERE
            Vogn_ID = ?
        ''', (id,)
    )
    return cursor.fetchone()[0]


def getTakenSeatsOnWagonForRouteOnDate(rute_id, dato):
    wagons = getWagons(rute_id)
    tickets = findTikcetsByRouteOnDate(rute_id, dato)
    
    taken_seats = []
    
    for ticket in tickets:
        pass    
    
    return taken_seats


def insertTicketsToDatabase(tickets):
    for ticket in tickets:
        cursor.execute(
            '''
            INSERT INTO Billett VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ticket.billett_id, ticket.plass_nr, 
                ticket.start_stasjon, ticket.slutt_stasjon, 
                ticket.ordrenummer, ticket.vogn_id, 
                ticket.billettype, ticket.indeks)
            ) 
        print(f"Inserted ticket {ticket.billett_id} into database")
    con.commit()
       
if __name__ == '__main__':
    orderTickets(1, "28/03/23", "Trondheim", "Bodø")
    #print(findLegalTickets(findRoute("03/04/23", "17:41", "Trondheim", "Bodø"), "Trondheim", "Bodø"))
    pass