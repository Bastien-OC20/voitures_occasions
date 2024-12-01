# FILE: streamlit/page/home_page.py

import os
import sys
import streamlit as st
from sqlalchemy.orm import Session
import plotly.express as px
import pandas as pd


# Ajouter le chemin du dossier parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from API.database import SessionLocal
from API.models import Vehicule

def show_home_page():
    st.header("Bienvenue sur le site de prédiction du Prix du Véhicule")
    st.write("""
    Ce site utilise des modèles de machine learning pour prédire le prix des véhicules d'occasion.
    Utilisez le menu pour naviguer vers la page de prédiction et obtenir une estimation du prix de votre véhicule.
    """)

    # Connexion à la base de données
    db = SessionLocal()
    vehicules = db.query(Vehicule).all()

    if vehicules:
        vehicule = vehicules[0]

        carburant_type = vehicule.carburant.type if vehicule.carburant else "N/A"
        transmission_type = vehicule.transmission.type if vehicule.transmission else "N/A"
        modele_nom = vehicule.modele.nom if vehicule.modele else "N/A"
        marque_nom = vehicule.marque.nom if vehicule.marque else "N/A"

        # Afficher les données
        st.subheader("Exemple d'un véhicule dans la base de données")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Marque: {marque_nom}")
            st.write(f"Modèle: {modele_nom}")
            st.write(f"Année: {vehicule.annee}")
            st.write(f"Kilométrage: {vehicule.kilometrage} km")
            st.write(f"Prix: {vehicule.prix} €")
        with col2:
            st.write(f"État: {vehicule.etat}")
            st.write(f"Carburant: {carburant_type}")
            st.write(f"Transmission: {transmission_type}")

        # Créer un DataFrame à partir des données des véhicules
        df = pd.DataFrame(
            [
                {
                    "Marque": v.marque.nom if v.marque else "N/A",
                    "Modèle": v.modele.nom if v.modele else "N/A",
                    "Année": v.annee,
                    "Prix": v.prix,
                    "Carburant": v.carburant.type if v.carburant else "N/A",
                    "Transmission": v.transmission.type if v.transmission else "N/A",
                }
                for v in vehicules
            ]
        )

        # Options de la barre latérale
        st.sidebar.header("Options de visualisation")
        graphique = st.sidebar.selectbox(
            "Choisissez un graphique à afficher",
            (
                "Prix des véhicules par année",
                "Prix moyen par marque",
                "Prix moyen par type de carburant",
                "Prix moyen par type de transmission",
            ),
        )

        if graphique == "Prix des véhicules par année":
            fig = px.scatter(
                df,
                x="Année",
                y="Prix",
                color="Marque",
                title="Prix des véhicules par année",
            )
            st.plotly_chart(fig)
        elif graphique == "Prix moyen par marque":
            df_marque = df.groupby("Marque")["Prix"].mean().reset_index()
            fig = px.bar(df_marque, x="Marque", y="Prix", title="Prix moyen par marque")
            st.plotly_chart(fig)
        elif graphique == "Prix moyen par type de carburant":
            df_carburant = df.groupby("Carburant")["Prix"].mean().reset_index()
            fig = px.bar(
                df_carburant,
                x="Carburant",
                y="Prix",
                title="Prix moyen par type de carburant",
            )
            st.plotly_chart(fig)
        elif graphique == "Prix moyen par type de transmission":
            df_transmission = df.groupby("Transmission")["Prix"].mean().reset_index()
            fig = px.bar(
                df_transmission,
                x="Transmission",
                y="Prix",
                title="Prix moyen par type de transmission",
            )
            st.plotly_chart(fig)
    else:
        st.write("Aucun véhicule trouvé dans la base de données.")

    db.close()

# Afficher la page d'accueil
show_home_page()
