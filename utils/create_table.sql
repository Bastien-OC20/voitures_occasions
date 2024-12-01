CREATE TABLE Marque (
    ID_Marque INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT NOT NULL
);

CREATE TABLE Carburant (
    ID_Carburant INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);

CREATE TABLE Transmission (
    ID_Transmission INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);

CREATE TABLE Modele (
    ID_Modele INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT NOT NULL,
    Marque_ID INTEGER,
    FOREIGN KEY (Marque_ID) REFERENCES Marque(ID_Marque)
);

CREATE TABLE Users (
    ID_User INTEGER PRIMARY KEY AUTOINCREMENT,
    Email TEXT NOT NULL UNIQUE,
    Nom TEXT NOT NULL,
    Password TEXT NOT NULL,
    Is_Active BOOLEAN NOT NULL DEFAULT 1,
    Is_Superuser BOOLEAN NOT NULL DEFAULT 0,
    Profile_Image TEXT
);

CREATE TABLE Vehicule (
    ID_Vehicule INTEGER PRIMARY KEY AUTOINCREMENT,
    Annee INTEGER,
    Kilometrage FLOAT,
    Prix FLOAT,
    Etat TEXT,
    Marque_ID INTEGER,
    Modele_ID INTEGER,
    Carburant_ID INTEGER,
    Transmission_ID INTEGER,
    FOREIGN KEY (Marque_ID) REFERENCES Marque(ID_Marque),
    FOREIGN KEY (Modele_ID) REFERENCES Modele(ID_Modele),
    FOREIGN KEY (Carburant_ID) REFERENCES Carburant(ID_Carburant),
    FOREIGN KEY (Transmission_ID) REFERENCES Transmission(ID_Transmission)
);