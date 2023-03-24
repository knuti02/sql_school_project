import sqlite3

# class for togrute
from util import create_connection
def finn_slutt_stasjon_for_rute(cursor, rute_id):
    cursor.execute(
        ''' SELECT
                start.rute_id,
                start.stasjon_ID, 
                slutt.stasjon_ID,
                navn
                
            FROM
                Stasjon_i_rute AS start
                JOIN
                Stasjon_i_rute AS slutt
                JOIN
                Stasjon
                
            WHERE
                start.rute_id = slutt.rute_id
                AND
                start.rute_id = ?
                AND
                start.sekvensnummer = (SELECT MIN(sekvensnummer) FROM Stasjon_i_rute WHERE rute_id = ?)
                AND
                slutt.sekvensnummer = (SELECT MAX(sekvensnummer) FROM Stasjon_i_rute WHERE rute_id = ?)
                AND
                slutt.stasjon_ID = Stasjon.stasjon_ID
        ''', (rute_id, rute_id, rute_id,)
    )
    
    return cursor.fetchone()


def finn_slutt_stasjon_for_alle_ruter(cursor):
    cursor.execute(
        '''
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
        
        '''
    )
    return cursor.fetchall()


def start_to_finish(cursor, start, finish, day):
    cursor.execute(
        '''
        SELECT DISTINCT
            start.rute_id,
            start.ankomsttid_avgangstid,
            finish.ankomsttid_avgangstid
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
        ''', (start, finish, day,)
    )
    return cursor.fetchall()



cursor = create_connection()[1]

print(start_to_finish(cursor, "Trondheim", "Bodø", "Mandag"))