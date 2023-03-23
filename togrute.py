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


def retrieve_based_on_time(cursor, tidspunkt):
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


def getPreviousDay(day):
    weekdays = getWeekdays()

    if weekdays.index(day) == 0:
        return weekdays[6]
    else:
        return weekdays[weekdays.index(day) - 1]


def retrieve_time_based_on_day(cursor, ukedag, stasjonNavn):
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
        return None
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

    return info_to_return


cursor = create_connection()[1]
print(retrieveTripFromStartToFinish(cursor, "Trondheim", "Bodø", "Mandag"))
# print(retrieve_time_based_on_day(cursor, "Mandag", "Trondheim"))
