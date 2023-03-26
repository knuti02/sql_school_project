import sqlite3

# class for togrute
from util import *


class Togrute:
    def __init__(self, togrute_id):
        self.togrute_id = togrute_id

# Brukerhistorie C: Bruker skal oppgi en Stasjon og dag,
#        også få opp alle togruter som går fra denne stasjonen på denne dagen
def retrieveTogrute(cursor, ukedag, stasjon) -> list:
    cursor.execute(
        '''
        SELECT
            t1.rute_id, 
            ankomsttid_avgangstid,
            navn 
                        
        FROM (
            SELECT 
                rute_id,
                ankomsttid_avgangstid
            
            FROM
                Stasjon
                NATURAL JOIN
                Stasjon_i_rute
                NATURAL JOIN
                Ukedag
                
            WHERE
                Navn_på_dag = ?
                AND
                navn = ?
            ) AS t1 JOIN (
            SELECT
                rute_id,
                navn
            FROM (
                SELECT 
                    rute_id, 
                    stasjon_id
                    
                FROM (
                    SELECT 
                        rute_id,
                        stasjon_id,
                        sekvensnummer, 
                        ROW_NUMBER() OVER (PARTITION BY rute_id ORDER BY sekvensnummer DESC) AS rute_nummer
                    FROM Stasjon_i_rute
                ) t
                WHERE rute_nummer = 1
                ) NATURAL JOIN
                Stasjon
            ) AS t2
        ON t1.rute_id = t2.rute_id
            

        ''', (ukedag, stasjon)
    )

    return cursor.fetchall()



# Brukerhistorie D: Bruker skal oppgi en Stasjon, sluttstasjon, dag og tid
#        også få opp alle togruter som passer.
def start_to_finish(cursor, start, finish, day, time):
    cursor.execute(
        '''
        SELECT DISTINCT
            start.rute_id,
            start.ankomsttid_avgangstid,
            finish.ankomsttid_avgangstid,
            start.navn_på_dag
        FROM 
            (
                SELECT
                    *
                FROM
                    Stasjon
                    JOIN
                    Stasjon_i_rute  
                    NATURAL JOIN
                    Ukedag   
                WHERE
                    navn = ?  
                    AND
                    Stasjon.stasjon_id = Stasjon_i_rute.stasjon_id 
                            
            ) AS start 
            JOIN 
            (
                SELECT
                    *
                FROM
                    Stasjon
                    JOIN
                    Stasjon_i_rute  
                    NATURAL JOIN
                    Ukedag
                WHERE
                    navn = ?  
                    AND
                    Stasjon.stasjon_id = Stasjon_i_rute.stasjon_id 
            ) AS finish
            ON start.rute_id = finish.rute_id
        WHERE 
            start.Navn_på_dag = ?
            AND
            start.sekvensnummer < finish.sekvensnummer
            AND
            start.ankomsttid_avgangstid >= (
                    SELECT
                        ankomsttid_avgangstid
                    FROM
                        Stasjon_i_rute
                    WHERE
                        ankomsttid_avgangstid >= ?
                    ORDER BY
                        ABS(strftime('%s', ?) - strftime('%s', ankomsttid_avgangstid))
            )
        ''', (start, finish, day, time, time)
    )
    return cursor.fetchall()
    

def print_routes_from_start_to_finish(cursor, start, finish, day, time):
    today = start_to_finish(cursor, start, finish, day, time)
    tomorrow = start_to_finish(cursor, start, finish, getNextDay(day), "00:00")
    
    print(f"Ruter fra {start} til {finish}:")
    for rute in today:
        print(f"{rute[3]}: Rute {rute[0]}, avgang {rute[1]}, ankomst {rute[2]}")
    for rute in tomorrow:
        print(f"{rute[3]}: Rute {rute[0]}, avgang {rute[1]}, ankomst {rute[2]}")



def retrieve_time_based_on_day(cursor, ukedag, stasjonNavn) -> list:
    # finn neste dag også
    next_day = getNextDay(ukedag)

    try:
        # Hent rutetider for stasjonen på gitt ukedag og etterfølgende dag
        cursor.execute(
            '''
            SELECT
                *

            FROM
                Stasjon
                NATURAL JOIN
                Ukedag
                NATURAL JOIN
                Stasjon_i_rute

            WHERE
                (
                    Navn_på_dag = ?
                    OR Navn_på_dag = ?
                )
                AND navn = ?

            ORDER BY CASE
                WHEN Navn_på_dag = ? THEN 0
                ELSE 1
            END, ankomsttid_avgangstid
            ''', (ukedag, next_day, stasjonNavn, ukedag)
        )
    except sqlite3.Error as e:
        print(e)
        return ["Exeption thrown"]
    info = cursor.fetchall()
    info_to_return = []

    # Sjekke om klokka har bikket 00:00 fra forrige stasjon, da skal neste dag skrives i stedet
    for tup in info:
        # hopp over sjekk hvis sekvensnummer er 1, og bare gi den sin dag
        if tup[6] == 1:
            info_to_return.append(
                [tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]])
            continue
        # Hent forrige stasjon
        cursor.execute(
            '''
            SELECT
                *

            FROM
                Stasjon_i_rute

            WHERE
                rute_id = ?
                AND
                sekvensnummer = (? - 1)
            ''', (tup[4], tup[6])
        )

        temp_info = cursor.fetchone()

        if temp_info[2].split(':')[0] > tup[5]:
            correctDay = getNextDay(tup[3])
        else:
            correctDay = tup[3]
        info_to_return.append(
            [tup[0], tup[1], tup[2], correctDay, tup[4], tup[5], tup[6]])

    return info_to_return


def retrieveTripFromStartToFinish(cursor, startStasjon, sluttStasjon, ukedag):
    startStasjon_info = retrieve_time_based_on_day(
        cursor, ukedag, startStasjon)

    previous_day = getPreviousDay(ukedag)
    startStasjon_previous_day = retrieve_time_based_on_day(
        cursor, previous_day, startStasjon)
    for start_tup in startStasjon_previous_day:
        # fjern de som ikke er på forrige dag fra denne lista
        if start_tup[3] != previous_day:
            startStasjon_previous_day.remove(start_tup)

    cursor.execute(
        '''
            SELECT
                *
                
            FROM
                Stasjon_i_rute
                NATURAL JOIN
                Stasjon

            WHERE
                navn = ?
            ''', (sluttStasjon, )
    )
    sluttStasjon_info = cursor.fetchall()

    # print("startStasjon_info: ", startStasjon_info,
    #      "sluttStasjon_info: ", sluttStasjon_info)

    info_to_return = []
    for start_tup in startStasjon_info:
        start_index = start_tup[6]

        for slutt_tup in sluttStasjon_info:
            slutt_index = slutt_tup[1]

            # sluttstasjon må komme etter (ha større sekvensnummer, og ruteID må være lik)
            if slutt_index > start_index and slutt_tup[0] == start_tup[4]:
                # returnerer starttid, sluttid og dag
                info_to_return.append(
                    (start_tup[5], slutt_tup[2], start_tup[3]))
    # Lik kode som over, bare for tidligere dag (for å få med nattog)
    for start_tup in startStasjon_previous_day:
        start_index = start_tup[6]

        for slutt_tup in sluttStasjon_info:
            slutt_index = slutt_tup[1]

            # sluttstasjon må komme etter (ha større sekvensnummer, og ruteID må være lik)
            if slutt_index > start_index and slutt_tup[0] == start_tup[4]:
                # returnerer starttid, sluttid og dag
                info_to_return.append(
                    (start_tup[5], slutt_tup[2], start_tup[3]))

    for tup in info_to_return:
        #slett hvis det er forrige dag
        if tup[2] == previous_day:
            info_to_return.remove(tup)
    return info_to_return


#given a station and a route, find its index
def findIndex(station_name, route_id):
    cursor.execute(
        '''
        SELECT
            sekvensnummer
        
        FROM
            Stasjon
            JOIN
            Stasjon_i_rute
            
        WHERE
            Stasjon.navn = ?
            AND
            Stasjon_i_rute.rute_ID = ?
            AND
            Stasjon.stasjon_ID = Stasjon_i_rute.stasjon_ID
        ''', (station_name, route_id)
    )
    return cursor.fetchone()[0]


cursor = create_connection()[1]

if __name__ == '__main__':
    print(findIndex("Mo i Rana", 1))
    
