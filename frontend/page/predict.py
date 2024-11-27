# FILE: front/pages/predict.py

import streamlit as st
import requests

def show_predict_page():
    st.title("Prédiction du Prix du Véhicule")

    # Créer un formulaire pour collecter les données du véhicule
    marque = st.text_input("Marque")
    modele = st.text_input("Modèle")
    annee = st.number_input("Année", min_value=1950, max_value=2100, step=1)
    kilometrage = st.number_input("Kilométrage", min_value=10000)
    etat = st.text_input("État", value="Occasion")
    carburant = st.selectbox("Carburant", ["Essence", "Diesel"])
    transmission = st.selectbox("Transmission", ["Manuelle", "Automatique"])

    if st.button("Prédire le Prix"):
        # Envoyer les données à l'API FastAPI
        data = {
            "kilometrage": kilometrage,
            "annee": annee,
            "marque": marque,
            "carburant": carburant,
            "transmission": transmission,
            "modele": modele,
            "etat": etat
        }
        response = requests.post("http://127.0.0.1:8000/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            if "random_forest_prediction" in result and "logistic_regression_evaluation" in result:
                st.success(f"Prédiction du prix: {result['random_forest_prediction']}")
                st.info(f"Évaluation du prix: {result['logistic_regression_evaluation']}")
            else:
                st.error("La réponse de l'API ne contient pas les clés attendues.")
        else:
            try:
                error_detail = response.json().get("detail", "Erreur inconnue")
                st.error(f"Erreur lors de la prédiction: {error_detail}")
            except ValueError:
                st.error("Erreur lors de la prédiction: Impossible de décoder la réponse de l'API")
