# FILE: front/pages/predict.py

import os
import sqlite3
import streamlit as st
from loguru import logger
from datetime import datetime, date
import requests
import time

# Configuration de loguru
logger.add("./frontend/log/predict.log", rotation="500 MB")

def fetch_vehicle_data():
    conn = sqlite3.connect('voitures_aramisauto.db')
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT Nom FROM Marque")
    marques = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Type FROM Carburant")
    carburants = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Type FROM Transmission")
    transmissions = [row[0] for row in cursor.fetchall()]

    conn.close()
    return marques, carburants, transmissions

def show_predict_page():
    st.title("Prédiction du Prix du Véhicule")

    # Récupérer les données du véhicule depuis la base de données
    marques, carburants, transmissions = fetch_vehicle_data()

    # Créer un formulaire pour collecter les données du véhicule
    marque = st.selectbox("Marque", marques)
    modele = st.text_input("Modèle")
    annee = st.date_input("Année", min_value=date(1950, 1, 1), max_value=date(2100, 12, 31)
    ).year
    kilometrage = st.slider("Kilométrage", min_value=1000, max_value=500000, step=1000)
    etat = st.text_input("État", value="Occasion")
    carburant = st.selectbox("Carburant", carburants)
    transmission = st.selectbox("Transmission", transmissions)

    if st.button("Prédire le Prix"):
        # Exemple de journalisation
        logger.info("Début de la prédiction")

        # Données envoyées à l'API FastAPI
        data = {
            "kilometrage": kilometrage,
            "annee": annee,
            "marque": marque,
            "carburant": carburant,
            "transmission": transmission,
            "modele": modele,
            "etat": etat
        }
        logger.debug(f"Données envoyées à l'API: {data}")

        response = requests.post("http://127.0.0.1:8000/predict", json=data)
        logger.debug(f"Réponse de l'API: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            logger.debug(f"Résultat de l'API: {result}")
            if "random_forest_prediction" in result and "logistic_regression_evaluation" in result:
                st.success(f"Prédiction du prix: {result['random_forest_prediction']}")
                if result['logistic_regression_evaluation'] == "mauvais prix":
                    result['logistic_regression_evaluation'] = "pas abordable"
                elif result['logistic_regression_evaluation'] == "bon prix":
                    result['logistic_regression_evaluation'] = "abordable"

                st.info(f" {result['logistic_regression_evaluation']} par rapport au prix du marché")

                # Générer un rapport de prédiction
                report_content = f"""
                Rapport de Prédiction
                ---------------------
                Marque: {marque}
                Modèle: {modele}
                Année: {annee}
                Kilométrage: {kilometrage}
                État: {etat}
                Carburant: {carburant}
                Transmission: {transmission}
                Prédiction du prix: {result['random_forest_prediction']}
                Évaluation: {result['logistic_regression_evaluation']}
                """
                report_dir = "./frontend/rapport/"
                os.makedirs(report_dir, exist_ok=True)
                report_name = f"{report_dir}rapport_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(report_name, "w") as file:
                    file.write(report_content)

                # Ajouter le rapport à la session
                if "reports" not in st.session_state:
                    st.session_state["reports"] = []
                st.session_state["reports"].append(report_name)

                # Permettre le téléchargement du rapport avec une barre de progression
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(percent_complete + 1)

                # Permettre le téléchargement du rapport
                with open(report_name, "rb") as file:
                    st.download_button(
                        label="Télécharger le rapport de prédiction",
                        data=file,
                        file_name=report_name,
                        mime="text/plain"
                    )
            else:
                logger.error("La réponse de l'API ne contient pas les clés attendues.")
                st.error("La réponse de l'API ne contient pas les clés attendues.")
        else:
            try:
                error_detail = response.json().get("detail", "Erreur inconnue")
                logger.error(f"Erreur lors de la prédiction: {error_detail}")
                st.error(f"Erreur lors de la prédiction: {error_detail}")
            except ValueError:
                logger.error("Erreur lors de la prédiction: Impossible de décoder la réponse de l'API")
                st.error("Erreur lors de la prédiction: Impossible de décoder la réponse de l'API")
