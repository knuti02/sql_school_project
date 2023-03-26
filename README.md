# Prosjekt Database

Initialiser databasen ved å kjøre ``python database.py``, slik vil all nødvendig informasjon bli fylt inn slik at programmet har info å ta utgangspunkt i.

Start programmet ved å kjøre ``python start_menu.py``

## Antakelser

* Vi antar at når en bruker søker etter togruter med et klokkeslett på en gitt dag,
  Så vil brukeren bare få opp ruter som går på eller etter klokkeslettet den dagen, men alle ruter dagen etter.

## Endringer
* Kundeordre har nå dato_for_tur slik at vi kan sjekke om en plass er ledig på en dato.
* Vi ga Kundeordre rute_id etter å ha glemt å legge det inn tidligere.
* I stasjon_i_rute ble to kolonner "ankomsttid" og "avgangstid", slått sammen til en "ankomsttid_avgangstid".
* Deler av databasen ble overflødig etter vi fikk jobbet videre med prosjektet. Disse er fortsatt med i innleveringen, men gjør ingenting utover å være i databasen. 

