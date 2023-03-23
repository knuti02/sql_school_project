from datetime import datetime

from util import create_connection
from kunde import Kunde, makeKunde, insertIntoTableKunde
from jernbane import Jernbane, retrieveStasjon, retrieve_all_stations
from togrute import Togrute, retrieveTogrute, retrieve_based_on_time, retrieve_time_based_on_day, retrieveTripFromStartToFinish

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
    print("Dette er bestillingssiden! \nFor å logge ut, skriv \"Q\"\n")
    print("Nordlandsbanen går mellom stasjonene: \n")
    # print(stations)
    for stasjon in stations:
        print(stasjon)

    print("\nRutene går på alle dagene i uka:\nMandag,\nTirsdag,\nOnsdag,\nTorsdag,\nFredag,\nLørdag,\nSøndag\n")

    while True:
        kunde_input = input(
            'For å se togruter, skriv: "STARTSTASJON, SLUTTSTASJON, DD/MM/ÅÅ":\n')
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

        except:
            print("Ugyldig input!")
            continue

        if start_stasjon not in stations:
            print("Ugyldig startstasjon!")
            continue
        if slutt_stasjon not in stations:
            print("Ugyldig sluttstasjon")
            continue

        # sjekk om stasjonene er i samme by
        if start_stasjon.lower == slutt_stasjon.lower:
            print("Start- og sluttstasjon kan ikke være like!")
            continue

        # Finn togruter
        liste_med_togruter_fra_stasjon_til_stasjon = retrieveTripFromStartToFinish(
            cursor, start_stasjon, slutt_stasjon, day_of_week)
        print(f"{start_stasjon} til {slutt_stasjon}:")
        for tup in liste_med_togruter_fra_stasjon_til_stasjon:
            print(f"{tup[2]}: {tup[0]} - {tup[1]}")

        print("Oppgi ønsket valg: \n")
