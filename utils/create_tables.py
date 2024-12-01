import sqlite3

# Chemin vers le fichier SQL
sql_file_path = 'create_table.sql'

# Se connecter à la base de données SQLite
conn = sqlite3.connect('../data/db/voitures_aramisauto_final.db')
cursor = conn.cursor()

# Lire le contenu du fichier SQL
with open(sql_file_path, 'r') as sql_file:
    sql_script = sql_file.read()

# Exécuter le script SQL
cursor.executescript(sql_script)

# Sauvegarder les modifications et fermer la connexion
conn.commit()
conn.close()

print("Tables créées avec succès.")