from util import create_connection
from kunde import Kunde, makeKunde, insertIntoTableKunde, retrieveKunde
from bestilling import bestilling

con, cursor = create_connection()

# Start program med "innlogging", ved å bare skrive inn navn og kunde ID


def program_loop():
    print("Velkommen til billettkjøp hos Nordlandsbanen!")
    start_input: str = ""

    while start_input not in ["R", "r", "L", "l"]:
        start_input = input(
            'Skriv "L" for å logge inn, eller "R" for å registrere bruker: \n')

    if start_input == "R" or start_input == "r":
        # Gå til registrering
        kunde = makeKunde(cursor, input("Skriv inn navn: "), input(
            "Skriv inn adresse: "), input("Skriv inn telefonnummer: "))
        insertIntoTableKunde(cursor, con, kunde)

        cursor.execute(
            '''SELECT MAX(kundenummer) FROM Kunde''')
        max_value = cursor.fetchone()[0]

        print(f"Din ID er {max_value}, denne må du huske for å logge inn!\n")
        program_loop()

    else:
        while True:
            kunde_input = input(
                "For å logge inn, skriv: 'KUNDENUMMER og NAVN': \n")

            try:
                kundenummer = int(kunde_input.split()[0])
            except:
                print("Ugyldig kundenummer!\n")
                continue

            navn = ' '.join(kunde_input.split()[1:])

            kunde = retrieveKunde(cursor, kundenummer)

            if kunde == None:
                print("Feil kundenummer eller navn, prøv igjen!\n")
                print("1")
                continue

            if kunde.navn != navn:
                print("Feil kundenummer eller navn, prøv igjen!\n")
                continue

            print("Logged in!\n")
            bestilling(kundenummer)

            break

    program_loop()


program_loop()
