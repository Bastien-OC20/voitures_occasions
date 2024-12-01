import pandas as pd
import sqlite3
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connexion à la base de données
conn = sqlite3.connect('../data/db/voitures_aramisauto_final.db')
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Carburant (
    ID_Carburant INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Transmission (
    ID_Transmission INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Marque (
    ID_Marque INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Modele (
    ID_Modele INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT NOT NULL,
    Marque_ID INTEGER NOT NULL,
    FOREIGN KEY (Marque_ID) REFERENCES Marque(ID_Marque)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Vehicule (
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
)
''')

# Chargement des données
df = pd.read_csv('../data/csv/voitures_aramisauto_cleaned.csv')

# Ajouter les colonnes Carburant_ID et Transmission_ID au DataFrame
carburants = df["Carburant"].unique()
carburant_map = {}
for carburant in carburants:
    cursor.execute("INSERT OR IGNORE INTO Carburant (type) VALUES (?)", (carburant,))
    cursor.execute("SELECT ID_Carburant FROM Carburant WHERE type = ?", (carburant,))
    carburant_id = cursor.fetchone()[0]
    carburant_map[carburant] = carburant_id
df["Carburant_ID"] = df["Carburant"].map(carburant_map)

transmissions = df["Transmission"].unique()
transmission_map = {}
for transmission in transmissions:
    cursor.execute("INSERT OR IGNORE INTO Transmission (type) VALUES (?)", (transmission,))
    cursor.execute("SELECT ID_Transmission FROM Transmission WHERE type = ?", (transmission,))
    transmission_id = cursor.fetchone()[0]
    transmission_map[transmission] = transmission_id
df["Transmission_ID"] = df["Transmission"].map(transmission_map)

# Insérer les Marques
marques = df["Marque"].unique()
for marque in marques:
    cursor.execute("INSERT OR IGNORE INTO Marque (Nom) VALUES (?)", (marque,))
    logger.info(f"Marque '{marque}' insérée ou déjà existante.")
conn.commit()
logger.info("Insertion des marques terminée.")

# Insérer les Modèles
modeles = df["Modele"].unique()
for modele in modeles:
    marque = df[df["Modele"] == modele]["Marque"].values[0].strip()
    cursor.execute("SELECT ID_Marque FROM Marque WHERE Nom = ?", (marque,))
    marque_id = cursor.fetchone()
    if marque_id:
        marque_id = marque_id[0]
        cursor.execute(
            "INSERT OR IGNORE INTO Modele (Nom, Marque_ID) VALUES (?, ?)",
            (modele, marque_id),
        )
        logger.info(f"Insertion du modèle '{modele}' pour la marque ID {marque_id}.")
    else:
        logger.error(f"Marque non trouvée pour le Modèle '{modele}'.")
conn.commit()
logger.info("Insertion des modèles terminée.")

# Insérer les Véhicules
for _, row in df.iterrows():
    marque = row["Marque"].strip()
    modele = row["Modele"].strip()

    # Récupérer l'ID de la marque
    cursor.execute("SELECT ID_Marque FROM Marque WHERE Nom = ?", (marque,))
    marque_id = cursor.fetchone()
    if not marque_id:
        logger.error(f"Marque '{marque}' non trouvée pour le véhicule.")
        continue
    marque_id = marque_id[0]

    # Récupérer l'ID du modèle
    cursor.execute(
        "SELECT ID_Modele FROM Modele WHERE Nom = ? AND Marque_ID = ?",
        (modele, marque_id),
    )
    modele_id = cursor.fetchone()
    if not modele_id:
        logger.error(f"Modèle '{modele}' non trouvé pour la marque ID {marque_id}.")
        continue
    modele_id = modele_id[0]

    # Insérer le véhicule
    cursor.execute(
        "INSERT INTO Vehicule (Annee, Kilometrage, Prix, Etat, Marque_ID, Modele_ID, Carburant_ID, Transmission_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            row["Annee"],
            row["Kilometrage"],
            row["Prix"],
            row["Etat"],
            marque_id,
            modele_id,
            row["Carburant_ID"],
            row["Transmission_ID"],
        ),
    )
    logger.info(f"Véhicule inséré : {row['Marque']} {row['Modele']} {row['Annee']}.")
conn.commit()
logger.info("Insertion des véhicules terminée.")

# Fermer la connexion
conn.close()
