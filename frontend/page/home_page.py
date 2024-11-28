# FILE: front/page/home_page.py

import streamlit as st
import requests


def show_home_page():
    st.header("Bienvenue sur le site de prédiction du Prix du Véhicule")
    st.write("""
    Ce site utilise des modèles de machine learning pour prédire le prix des véhicules d'occasion.
    Utilisez le menu pour naviguer vers la page de prédiction et obtenir une estimation du prix de votre véhicule.
    """)

    # Faire une requête HTTP à l'API FastAPI pour récupérer les données
    response = requests.get("http://127.0.0.1:8000/vehicules/")
    if response.status_code == 200:
        vehicules = response.json()
        vehicule = [vehicules[0]] if vehicules else []

        carburant_type = (
                        vehicule["carburant"]["type"]
                        if "carburant" in vehicule and "type" in vehicule["carburant"]
                        else "N/A"
                    )
        transmission_type = (
                        vehicule["transmission"]["type"]
                        if "transmission" in vehicule and "type" in vehicule["transmission"]
                        else "N/A"
                    )

        # Afficher les données
        st.subheader("Véhicules dans la base de données")
        col1, col2 = st.columns(2)
        with col1:
            for vehicule in vehicules[:3]: 
                carburant_type = (
                        vehicule["carburant"]["type"]
                        if "carburant" in vehicule and "type" in vehicule["carburant"]
                        else "N/A"
                    )
                transmission_type = (
                        vehicule["transmission"]["type"]
                        if "transmission" in vehicule and "type" in vehicule["transmission"]
                        else "N/A"
                    )
                st.markdown(f"**Modèle**: {vehicule['modele']}")
                st.markdown(f"**Année**: {vehicule['annee']}")
                st.markdown(f"**Prix**: {vehicule['prix']} €")
                st.markdown(f"**Kilométrage**: {vehicule['kilometrage']} km")
                st.markdown(f"**Carburant**: {carburant_type}")
                st.markdown(f"**Transmission**: {transmission_type}")
                st.markdown(f"**État**: {vehicule['etat']}")
                st.divider()
        with col2:
            st.image("./frontend/img/logos_voitures.png", use_container_width=True)
    else:
        st.error("Erreur lors de la récupération des données.")
