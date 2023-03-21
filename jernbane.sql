CREATE TABLE "Stasjon" (
	"stasjon_ID"	INTEGER,
	"navn"	VARCHAR(50),
	"MOH"	FLOAT,
	PRIMARY KEY("stasjon_ID")
);

CREATE TABLE "Stasjon_i_rute" (
	"rute_ID"	INTEGER,
	"stasjon_ID"	INTEGER,
	"ankomsttid"	TIME,
	"avgangstid"	TIME,
	"sekvensnummer"	INTEGER,
	FOREIGN KEY("rute_ID") REFERENCES "Togrute"("rute_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("stasjon_ID") REFERENCES "Stasjon"("stasjon_ID") ON UPDATE CASCADE ON DELETE CASCADE
    PRIMARY KEY("rute_ID","stasjon_ID")
);

CREATE TABLE "Togrute" (
	"rute_ID"	INTEGER,
	"strekning_navn"	VARCHAR(50),
	"Vognoppsett_ID"	INTEGER,
	PRIMARY KEY("rute_ID"),
	FOREIGN KEY("strekning_navn") REFERENCES "Banestrekning"("strekning_navn") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Vognoppsett_ID") REFERENCES "VognOppsett"("Vognoppsett_ID") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Ukedag" (
	"Navn_på_dag"	VARCHAR(10),
	"rute_ID"	INTEGER,
	FOREIGN KEY("rute_ID") REFERENCES "Togrute"("rute_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Navn_på_dag","rute_ID")
);

CREATE TABLE "Delstrekning" (
	"Sportype"	VARCHAR(50),
	"Lengde"	INTEGER,
	"strekning_ID"	INTEGER,
	"StasjonEn_ID"	INTEGER,
	"StasjonTo_ID"	INTEGER,
	FOREIGN KEY("StasjonTo_ID") REFERENCES "Stasjon"("stasjon_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("StasjonEn_ID","StasjonTo_ID"),
	FOREIGN KEY("strekning_ID") REFERENCES "Banestrekning"("strekning_navn") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("StasjonEn_ID") REFERENCES "Stasjon"("stasjon_ID") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Banestrekning" (
	"strekning_navn"	VARCHAR(50),
	"framdriftsmiddel"	VARCHAR(50),
	"operatør_ID"	INTEGER,
	"StartStasjon_ID"	INTEGER,
	"SluttStasjon_ID"	INTEGER,
	FOREIGN KEY("operatør_ID") REFERENCES "Operatør"("operatør_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("strekning_navn"),
	FOREIGN KEY("StartStasjon_ID") REFERENCES "Stasjon"("stasjon_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("SluttStasjon_ID") REFERENCES "Stasjon"("stasjon_ID") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Operatør" (
	"operatør_ID"	INTEGER,
	"operatør_navn"	VARCHAR(50),
	PRIMARY KEY("operatør_ID")
);

CREATE TABLE "Kunderegister" (
	"operatør_ID"	INTEGER,
	"kundenummer"	INTEGER,
	PRIMARY KEY("operatør_ID","kundenummer"),
	FOREIGN KEY("operatør_ID") REFERENCES "Operatør"("operatør_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("kundenummer") REFERENCES "Kunde"("kundenummer") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Kunde" (
	"kundenummer"	INTEGER,
	"navn"	VARCHAR(50),
	"epostadresse"	VARCHAR(50),
	"mobilnummer"	INTEGER,
	PRIMARY KEY("kundenummer")
);

CREATE TABLE "Kundeordre" (
	"ordrenummer"	INTEGER,
	"dag"	VARCHAR(50),
	"tid"	TIME,
	"kundenummer"	INTEGER,
	PRIMARY KEY("ordrenummer"),
	FOREIGN KEY("kundenummer") REFERENCES "Kunde"("kundenummer") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Billett" (
	"Billett_ID"	INTEGER,
	"Plass_nr"	INTEGER,
	"StartStasjon_ID"	INTEGER,
	"SluttStasjon_ID"	INTEGER,
	"ordrenummer"	INTEGER,
	"Vogn_ID"	INTEGER,
	"Billettype"	VARCHAR(50),
	FOREIGN KEY("StartStasjon_ID") REFERENCES "Stasjon"("stasjon_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("SluttStasjon_ID") REFERENCES "Stasjon"("stasjon_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Billett_ID"),
	FOREIGN KEY("Vogn_ID") REFERENCES "Vogn"("Vogn_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("ordrenummer") REFERENCES "Kundeordre"("ordrenummer") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Sittebillett" (
	"Billett_ID"	INTEGER,
	FOREIGN KEY("Billett_ID") REFERENCES "Billett"("Billett_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Billett_ID")
);

CREATE TABLE "Sovebillett" (
	"Billett_ID"	INTEGER,
	PRIMARY KEY("Billett_ID"),
	FOREIGN KEY("Billett_ID") REFERENCES "Billett"("Billett_ID") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Soveplass_I_Vogn" (
	"Billett_ID"	INTEGER,
	"Vogn_ID"	INTEGER,
	"Kupénummer"	INTEGER,
	PRIMARY KEY("Billett_ID","Vogn_ID","Kupénummer"),
	FOREIGN KEY("Vogn_ID") REFERENCES "Vogn"("Vogn_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Kupénummer") REFERENCES "Sovekupé"("Kupenummér") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Billett_ID") REFERENCES "Sovebillett"("Billett_ID") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Sovekupé" (
	"Kupenummér"	INTEGER,
	"Vogn_ID"	INTEGER,
	PRIMARY KEY("Kupenummér","Vogn_ID"),
	FOREIGN KEY("Vogn_ID") REFERENCES "Vogn"("Vogn_ID") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Vogn" (
	"Vogn_ID"	INTEGER,
	"antall_plasser"	INTEGER,
	"Vogntype"	VARCHAR(50),
	PRIMARY KEY("Vogn_ID")
);

CREATE TABLE "Sittevogn" (
	"Vogn_ID"	INTEGER,
	PRIMARY KEY("Vogn_ID"),
	FOREIGN KEY("Vogn_ID") REFERENCES "Vogn"("Vogn_ID") ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE "Sovevogn" (
	"Vogn_ID"	INTEGER,
	FOREIGN KEY("Vogn_ID") REFERENCES "Vogn"("Vogn_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("Vogn_ID")
);

CREATE TABLE "VognOppsett" (
	"Vognoppsett_ID"	INTEGER,
	PRIMARY KEY("Vognoppsett_ID")
);

CREATE TABLE "InneholderVogn" (
	"Vognoppsett_ID"	INTEGER,
	"Vogn_ID"	INTEGER,
	"Index"	INTEGER,
	PRIMARY KEY("Vognoppsett_ID","Vogn_ID", "Index"),
	FOREIGN KEY("Vognoppsett_ID") REFERENCES "VognOppsett"("Vognoppsett_ID") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("Vogn_ID") REFERENCES "Vogn"("Vogn_ID") ON UPDATE CASCADE ON DELETE CASCADE
);