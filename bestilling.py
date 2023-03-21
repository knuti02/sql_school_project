from datetime import datetime

from connection import create_connection
from kunde import Kunde, makeKunde, insertIntoTableKunde

con, cursor = create_connection()
eng_to_nor ={
    "Monday" : "Mandag",
    "Tuesday" : "Tirsdag",
    "Wednesday" : "Onsdag",
    "Thursday" : "Torsdag",
    "Friday" : "Fredag",
    "Saturday" : "Lørdag",
    "Sunday" : "Søndag" 
}   

# Start program med "innlogging", ved å bare skrive inn navn og kunde ID
def bestilling(kundenummer):
    print("Dette er bestillingssiden! \nFor å logge ut, skriv \"Q\"\n")
    print("Nordlandsbanen går mellom stasjonene: \nTrondheim,\nSteinkjer,\nMosjøen,\nMo i Rana,\nFauske,\nBodø\n\n")  
    print("Disse går på alle dagene i uka: \nTrondheim,\nSteinkjer,\nMosjøen,\nMo i Rana,\nFauske,\nBodø\n\n")

    while True:
        kunde_input = input('For å se togruter, skriv: "STARTSTASJON, SLUTTSTASJON, DD/MM/ÅÅ":\n')
        if kunde_input == "Q" or kunde_input == "q":
            return
        
        input_list = kunde_input.split(", ")
        
        try:
            start_stasjon = input_list[0]
            slutt_stasjon = input_list[1]
            dato = input_list[2]
            
            date_obj = datetime.strptime(dato, "%d/%m/%y")
            day_of_week = date_obj.strftime("%A") 
            day_of_week = eng_to_nor[day_of_week]  
            
            print(day_of_week)
            
        except:
            print("Noe ble feil, prøv igjen!")
            continue
            
        
    

