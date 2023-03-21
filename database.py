import sqlite3

con = sqlite3.connect("jernbane.db")

cursor = con.cursor()
cursor.execute("SELECT * FROM sqlite_master")


def insertIntoTableBanstrekning():
    # Banestrekning
    cursor.execute(
        '''INSERT INTO Banestrekning VALUES ('Nordlandsbanen', 'Diesel', '1', '1', '6')''')

    con.commit()


def insertIntoTableStasjoner():
    # Stasjoner
    cursor.execute(
        '''INSERT INTO Stasjon VALUES ('1', 'Trondheim', '5.1')''')
    cursor.execute(
        '''INSERT INTO Stasjon VALUES ('2', 'Steinkjer', '3.6')''')
    cursor.execute(
        '''INSERT INTO Stasjon VALUES ('3', 'Mosjøen', '6.8')''')
    cursor.execute(
        '''INSERT INTO Stasjon VALUES ('4', 'Mo i Rana', '3.5')''')
    cursor.execute(
        '''INSERT INTO Stasjon VALUES ('5', 'Fauske', '34.0')''')
    cursor.execute(
        '''INSERT INTO Stasjon VALUES ('6', 'Bodø', '4.1')''')

    con.commit()


def insertIntoTableDelstrekning():
    # Stasjoner
    cursor.execute(
        '''INSERT INTO Delstrekning VALUES ('Dobbel', '120', '1', '1', '2')''')
    cursor.execute(
        '''INSERT INTO Delstrekning VALUES ('Enkel', '280', '1', '2', '3')''')
    cursor.execute(
        '''INSERT INTO Delstrekning VALUES ('Enkel', '90', '1', '3', '4')''')
    cursor.execute(
        '''INSERT INTO Delstrekning VALUES ('Enkel', '170', '1', '4', '5')''')
    cursor.execute(
        '''INSERT INTO Delstrekning VALUES ('Enkel', '60', '1', '5', '6')''')

    con.commit()
    # con.close()


def insertIntoTableVogn():
    # Stasjoner
    cursor.execute(
        '''INSERT INTO Vogn VALUES ('1', '12', 'Sittevogn')''')
    cursor.execute(
        '''INSERT INTO Vogn VALUES ('2', '8', 'Sovevogn')''')

    con.commit()
    # con.close()


def insertIntoTableVognoppsett():
    # Vognoppsett
    cursor.execute(
        '''INSERT INTO Vognoppsett VALUES ('1')''')
    cursor.execute(
        '''INSERT INTO Vognoppsett VALUES ('2')''')
    cursor.execute(
        '''INSERT INTO Vognoppsett VALUES ('3')''')

    con.commit()


def insertIntoTableSittevogn():
    # Sovevogn
    cursor.execute(
        '''INSERT INTO Sittevogn VALUES ('1')''')

    con.commit()


def insertIntoTableSovevogn():
    # Sovevogn
    cursor.execute(
        '''INSERT INTO Sovevogn VALUES ('2')''')

    con.commit()


def insertIntoTableInneholderVogn():
    # Sovevogn
    cursor.execute(
        '''INSERT INTO InneholderVogn VALUES ('1', '1', '1')''')
    cursor.execute(
        '''INSERT INTO InneholderVogn VALUES ('1', '1', '2')''')
    cursor.execute(
        '''INSERT INTO InneholderVogn VALUES ('2', '1', '1')''')
    cursor.execute(
        '''INSERT INTO InneholderVogn VALUES ('2', '2', '2')''')
    cursor.execute(
        '''INSERT INTO InneholderVogn VALUES ('3', '1', '1')''')

    con.commit()


def insertIntoTableTogrute():
    # Sovevogn
    cursor.execute(
        '''INSERT INTO Togrute VALUES ('1', 'Nordlandsbanen', '1')''')
    cursor.execute(
        '''INSERT INTO Togrute VALUES ('2', 'Nordlandsbanen', '2')''')
    cursor.execute(
        '''INSERT INTO Togrute VALUES ('3', 'Nordlandsbanen', '3')''')

    con.commit()


def insertIntoTableStasjonIRute():
    # Sovevogn
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('1', '1', '07:49', '1')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('1', '2', '09:51', '2')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('1', '3', '13:20', '3')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('1', '4', '14:31', '4')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('1', '5', '16:49', '5')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('1', '6', '17:34', '6')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('2', '1', '23:05', '1')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('2', '2', '00:57', '2')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('2', '3', '04:41', '3')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('2', '4', '05:55', '4')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('2', '5', '08:19', '5')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('2', '6', '09:05', '6')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('3', '4', '08:11', '1')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('3', '3', '09:14', '2')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('3', '2', '12:31', '3')''')
    cursor.execute(
        '''INSERT INTO Stasjon_i_rute VALUES ('3', '1', '14:13', '4')''')

    con.commit()


def insertIntoTableUkedag():
    # Sovevogn
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Mandag', '1')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Tirsdag', '1')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Onsdag', '1')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Torsdag', '1')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Fredag', '1')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Mandag', '2')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Tirsdag', '2')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Onsdag', '2')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Torsdag', '2')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Fredag', '2')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Lørdag', '2')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Søndag', '2')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Mandag', '3')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Tirsdag', '3')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Onsdag', '3')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Torsdag', '3')''')
    cursor.execute(
        '''INSERT INTO Ukedag VALUES ('Fredag', '3')''')

    con.commit()


# insertIntoTableBanstrekning()

# insertIntoTableStasjoner()

# insertIntoTableDelstrekning()

# insertIntoTableSittevogn()

# insertIntoTableSovevogn()

# insertIntoTableVogn()

# insertIntoTableVognoppsett()

# insertIntoTableInneholderVogn()

# insertIntoTableTogrute()

# insertIntoTableStasjonIRute()

# insertIntoTableUkedag()


con.close()
