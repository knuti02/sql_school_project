import sqlite3

# class for togrute
from util import create_connection, getWeekdays


class Togrute:
    def __init__(self, togrute_id):
        self.togrute_id = togrute_id





def retrieveTogrute(cursor, ukedag):
    weekdays = getWeekdays()
    
    if weekdays.index(ukedag) == 6:
        ukedag2 = -1
    else:
        ukedag2 = weekdays[weekdays.index(ukedag) + 1]

    try:
        cursor.execute(
            '''
            SELECT
                *

            FROM
                Togrute
                NATURAL JOIN
                Ukedag

            WHERE
                Navn_på_dag = ?


            ''', (ukedag,)
        )
    except sqlite3.Error as e:
        print(e)
        return None

    info = cursor.fetchall()
    return info
    # return Togrute(togrute_id)  # , navn, vognoppsett_id)


# print(retrieveTogrute(cursor=cursor, ukedag='Mandag'))


def retrieve_based_on_time(cursor, tidspunkt):
    weekdays = getWeekdays()
    
    try:
        cursor.execute(
            '''
            SELECT
                *

            FROM
                Stasjon_i_rute

            WHERE
                ankomsttid_avgangstid = (
                    SELECT
                        ankomsttid_avgangstid
                    FROM
                        Stasjon_i_rute
                    WHERE
                        ankomsttid_avgangstid >= ?
                    ORDER BY
                        ABS(strftime('%s', ?) - strftime('%s', ankomsttid_avgangstid))
                    LIMIT 1
                )


            ''', (tidspunkt, tidspunkt)  # Finds closest time to the given time, that is not less than inputted time
        )
    except sqlite3.Error as e:
        print(e)
        return None

    info = cursor.fetchall()
    return info




def getNextDay(day):
    weekdays = getWeekdays()
    
    if weekdays.index(day) == 6:
        return weekdays[0]
    else:
        return weekdays[weekdays.index(day) + 1]


def retrieve_time_based_on_day(cursor, ukedag, stasjonNavn):
    # finn neste dag også
    weekdays = getWeekdays()

    if weekdays.index(ukedag) == 6:
        ukedag2 = weekdays[0]
    else:
        ukedag2 = weekdays[weekdays.index(ukedag) + 1]

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
            ''', (ukedag, ukedag2, stasjonNavn, ukedag)
        )
    except sqlite3.Error as e:
        print(e)
        return None
    info = cursor.fetchall()
    print(info)
    info_to_return = []

    for tup in info:
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
        print(temp_info)

        if temp_info[2].split(':')[0] > tup[5]:
            correctDay = getNextDay(tup[3])
        else:
            correctDay = tup[3]
        info_to_return.append(
            [tup[0], tup[1], tup[2], correctDay, tup[4], tup[5], tup[6]])

    return info_to_return

