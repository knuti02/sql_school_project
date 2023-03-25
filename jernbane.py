# class for kunde
class Jernbane:
    def __init__(self, stasjon_id, navn, moh):
        self.stasjon_id = stasjon_id
        self.navn = navn
        self.moh = moh


def retrieveStasjon(cursor, stasjon_id):
    try:
        cursor.execute(
            '''SELECT * FROM Stasjon WHERE stasjon_id = ?''',
            (stasjon_id,)
        )
    except:
        return None

    info = cursor.fetchone()

    navn = info[1]
    moh = info[2]

    return Jernbane(stasjon_id, navn, moh)


def retrieve_all_stations(cursor):
    try:
        cursor.execute(
            '''SELECT * FROM Stasjon'''
        )
    except:
        return []

    info = cursor.fetchall()

    stations = []
    for i in info:
        stations.append(i[1])

    return stations
