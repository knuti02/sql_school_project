from datetime import datetime

from util import *
from jernbane import retrieve_all_stations
from togrute import *
from billett import *
from orders import viewOrders

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

stations = retrieve_all_stations(cursor)

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
                'For å se togruter, skriv 1. \nFor å se togruter mellom to stasjoner, skriv 2. \nFor å bestille billett, skriv 3. \nFor å se bestillinger, skriv 4. \nFor å logge ut, skriv 5. \n')
        
        if valg == "1":
            se_togruter(stations)
            
        elif valg == "2":
            start_stasjon = ""
            while start_stasjon not in stations:
                
                start_stasjon = input("Hvilken stasjon vil du reise fra?:\n")
                if start_stasjon not in stations:
                    print("Stasjonen finnes ikke!")
            slutt_stasjon = ""
            while slutt_stasjon not in stations:
                
                slutt_stasjon = input("Hvilken stasjon skal du reise til?:\n")
                if slutt_stasjon not in stations:
                    print("Stasjonen finnes ikke!")

            dato = input("Når skal du reise? (dd/mm/yy):\n")
            day = getWeekdayBasedOnDate(dato)
            
            kl = input("Hvilken tid vil du reise? (hh:mm):\n")
            
            print_routes_from_start_to_finish(cursor, start_stasjon, slutt_stasjon, day, kl)
            
        elif valg == "3":
            dato = input("Når skal du reise? (dd/mm/yy):\n")
            
            start_stasjon = ""
            while start_stasjon not in stations:
                
                start_stasjon = input("Hvilken stasjon vil du reise fra?:\n")
                if start_stasjon not in stations:
                    print("Stasjonen finnes ikke!")
            slutt_stasjon = ""
            while slutt_stasjon not in stations:
                
                slutt_stasjon = input("Hvilken stasjon skal du reise til?:\n")
                if slutt_stasjon not in stations:
                    print("Stasjonen finnes ikke!")
            
            orderTickets(kundenummer, dato, start_stasjon, slutt_stasjon)
            
        elif valg == "4":
            viewOrders(kundenummer)
            
        elif valg == "5":
            return
            

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
