from datetime import datetime

from util import *
from jernbane import retrieve_all_stations
from togrute import *
from billett import *

con, cursor = create_connection()
eng_to_nor = {
    "Monday": "Mandag",
    "Tuesday": "Tirsdag",
    "Wednesday": "Onsdag",
    "Thursday": "Torsdag",
    "Friday": "Fredag",
    "Saturday": "Lørdag",
    "Sunday": "Søndag"
}

# Start program med "innlogging", ved å bare skrive inn navn og kunde ID


def bestilling(kundenummer):
    stations = retrieve_all_stations(cursor)
    print("Dette er bestillingssiden!")
    print("Nordlandsbanen går mellom stasjonene: \n")
    # print(stations)
    for stasjon in stations:
        print(stasjon)

    print("\nRutene går på alle dagene i uka:\nMandag,\nTirsdag,\nOnsdag,\nTorsdag,\nFredag,\nLørdag,\nSøndag\n")

    while True:
        valg = input(
                'For å se togruter, skriv 1. \nFor å bestille billett, skriv 2. \nFor å se bestillinger, skriv 3. \nFor å logge ut, skriv 4. \n')
        
        if valg == "1":
            se_togruter(stations)
            
        elif valg == "2":
            dato = input("Når skal du reise? (dd/mm/yy):\n")
            start_stasjon = input("Fra hvilken stasjon vil du reise fra?:\n")
            slutt_stasjon = input("Til hvilken stasjon skal du reise til?:\n")
            
            orderTickets(kundenummer, dato, start_stasjon, slutt_stasjon)
            
        

def se_togruter(stations):

    while True:
        kunde_input = input(
                'For å se togruter, skriv: "STARTSTASJON, Dag":\nFor å gå tilbake, skriv "Q"\n')
        if kunde_input == "Q" or kunde_input == "q":
            return

        input_list = kunde_input.split(", ")

        try:
            start_stasjon = input_list[0]
            day_of_week = input_list[1]
            # dato = input_list[2]

            # date_obj = datetime.strptime(dato, "%d/%m/%y")
            # day_of_week = date_obj.strftime("%A")
            # day_of_week = eng_to_nor[day_of_week]

        except:
            print("Ugyldig input!")
            return

        if start_stasjon not in stations:
            print("Ugyldig startstasjon!")
            return

        # Finn togruter
        liste_med_togruter_fra_stasjon_til_stasjon = retrieveTogrute(
            cursor, day_of_week, start_stasjon)
        print(f"\nAvganger fra {start_stasjon} på {day_of_week}:")
        for togrute in liste_med_togruter_fra_stasjon_til_stasjon:
            if togrute[2] == start_stasjon:
                continue
            print(f"Togrute {togrute[0]}: går {togrute[1]} mot {togrute[2]}")
        print("")    


if __name__ == "__main__":
    bestilling(1)
