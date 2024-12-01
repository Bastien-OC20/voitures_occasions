# FILE: streamlit/pages/predict.py

import os
import sys
import streamlit as st
from loguru import logger
from datetime import date
import requests
from sqlalchemy.orm import Session

# Ajouter le chemin du dossier parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from API.database import SessionLocal
from API.models import Vehicule, Marque, Modele, Carburant, Transmission

# Configuration de loguru
logger.add("./streamlit/log/predict.log", rotation="500 MB")

def fetch_vehicle_data():
    # Connexion à la base de données
    db = SessionLocal()

    marques = db.query(Marque).all()
    modeles = db.query(Modele).all()
    carburants = db.query(Carburant).all()
    transmissions = db.query(Transmission).all()

    db.close()

    marques = [marque.nom for marque in marques]
    modeles = [modele.nom for modele in modeles]
    carburants = [carburant.type for carburant in carburants]
    transmissions = [transmission.type for transmission in transmissions]

    return marques, modeles, carburants, transmissions

def show_predict_page():
    st.title("Prédiction du Prix du Véhicule")

    # Récupérer les données du véhicule depuis la base de données
    marques, modeles, carburants, transmissions = fetch_vehicle_data()

    # Interface utilisateur pour la prédiction
    marque = st.selectbox("Marque", marques)
    modele = st.selectbox("Modèle", modeles)
    carburant = st.selectbox("Carburant", carburants)
    transmission = st.selectbox("Transmission", transmissions)
    annee = st.number_input("Année", min_value=1900, max_value=date.today().year, value=2022)
    kilometrage = st.number_input("Kilométrage", min_value=0, value=10000)
    etat = st.selectbox("État", ["Neuf", "Occasion"])

    if st.button("Prédire le prix"):
        # Faire une requête à l'API pour obtenir la prédiction
        prediction_response = requests.post(
            "http://127.0.0.1:8000/predict/",
            json={
                "marque": marque,
                "modele": modele,
                "carburant": carburant,
                "transmission": transmission,
                "annee": annee,
                "kilometrage": kilometrage,
                "etat": etat,
            },
        )

        if prediction_response.status_code == 200:
            prediction_data = prediction_response.json()
            if "Gradient_Boosting_prediction" in prediction_data and "Logistic_Regression_evaluation" in prediction_data:
                prediction = prediction_data["Gradient_Boosting_prediction"]
                evaluation = prediction_data["Logistic_Regression_evaluation"]
                st.success(f"Le prix prédit pour ce véhicule est d'environ de {int(prediction)} €")
                st.info(f"{evaluation} par rapport au prix du marché")
                # Générer le rapport
                report_content = f"""
                Rapport de Prédiction du Prix du Véhicule

                Marque: {marque}
                Modèle: {modele}
                Carburant: {carburant}
                Transmission: {transmission}
                Année: {annee}
                Kilométrage: {kilometrage} km
                État: {etat}

                Prix prédit: {prediction} €
                Évaluation de l'abordabilité: {evaluation}
                """

                # Créer le dossier rapport s'il n'existe pas
                os.makedirs("rapport", exist_ok=True)

                # Enregistrer le rapport dans un fichier texte
                report_path = os.path.join(
                    "./streamlit/rapport", f"rapport_{marque}_{modele}_{date.today()}.txt"
                )
                with open(report_path, "w") as report_file:
                    report_file.write(report_content)

                # Offrir une option de téléchargement
                st.download_button(
                    label="Télécharger le rapport",
                    data=report_content,
                    file_name=f"rapport_{marque}_{modele}_{date.today()}.txt",
                    mime="text/plain",
                )
            else:
                st.error("La réponse de l'API ne contient pas les clés attendues.")
        else:
            st.error("Erreur lors de la prédiction du prix")

# Afficher la page de prédiction
show_predict_page()
