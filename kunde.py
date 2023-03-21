#class for kunde
class Kunde:
    def __init__(self, kunde_id, navn, adresse, telefonnummer):
        self.kunde_id = kunde_id
        self.navn = navn
        self.adresse = adresse
        self.telefonnummer = telefonnummer
 
#lag kunde. første kunde får kundenummer 0, andre 1 osv.    
def makeKunde(cursor, navn, adresse, telefonnummer):
    try:
        cursor.execute(
            '''SELECT MAX(kundenummer) FROM Kunde''')
        
        max_value = cursor.fetchone()[0]
    except:
        max_value = -1
    
    return Kunde(max_value + 1, navn, adresse, telefonnummer)

# legg kunde inn i Kunde og Kunderegister
def insertIntoTableKunde(cursor, con, kunde: Kunde):
    cursor.execute(
        '''INSERT INTO Kunde VALUES (?, ?, ?, ?)''', 
        (kunde.kunde_id, kunde.navn, kunde.adresse, kunde.telefonnummer)
    )
    
    cursor.execute(
        '''INSERT INTO Kunderegister VALUES (?, ?)''',
        (1, kunde.kunde_id)
    )
    
    con.commit()
    
def retrieveKunde(cursor, kunde_id):
    try:
        cursor.execute(
            '''SELECT * FROM Kunde WHERE kundenummer = ?''', 
            (kunde_id,)
        )
    except:
        return None
    
    info = cursor.fetchone()
    
    navn = info[1]
    adresse = info[2]
    telefonnummer = info[3]
    
    return Kunde(kunde_id, navn, adresse, telefonnummer)