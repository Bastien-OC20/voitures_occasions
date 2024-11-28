import streamlit as st
from sqlalchemy.orm import Session
from auth import get_db, signup, login
from API.models import User
import sys
import os
import requests
from fastapi import HTTPException
from PIL import Image
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Page principale de l'application
def main():
    st.title("Application de Prédiction des Voitures d'Occasion")
    current_directory = os.path.dirname(__file__)
    logo_path = os.path.join(current_directory, "logo_voiture.png")
    
    try:
        image = Image.open(logo_path)
        resized_image = image.resize((400, int(400 * image.height / image.width)))
        st.image(resized_image)
    except FileNotFoundError:
        st.error("L'image spécifiée n'a pas été trouvée. Veuillez vérifier le chemin.")
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image : {e}")

    # Vérifier si l'utilisateur est connecté
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'redirect' not in st.session_state:
        st.session_state['redirect'] = None

    # Si l'utilisateur est connecté
    if st.session_state['logged_in']:
        # Afficher la barre de navigation spécifique aux utilisateurs connectés
        user_menu = ["Recherche de Véhicule", "Mon Compte", "Déconnexion"]
        user_choice = st.sidebar.selectbox("Menu Utilisateur", user_menu)

        if user_choice == "Recherche de Véhicule":
            st.session_state['redirect'] = "prediction"
        elif user_choice == "Mon Compte":
            st.session_state['redirect'] = "account"
        elif user_choice == "Déconnexion":
            # Réinitialiser les paramètres de session pour déconnecter l'utilisateur
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.session_state['nom'] = None
            st.session_state['redirect'] = "login"

    else:
        # Navigation entre inscription et connexion pour les utilisateurs non connectés
        menu = ["Inscription", "Connexion"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Inscription":
            st.session_state['redirect'] = "signup"
        elif choice == "Connexion":
            st.session_state['redirect'] = "login"

    # Rediriger vers la page appropriée
    if st.session_state['redirect'] == "signup":
        show_signup_page()
    elif st.session_state['redirect'] == "login":
        show_login_page()
    elif st.session_state['redirect'] == "prediction":
        show_prediction_page()
    elif st.session_state['redirect'] == "account":
        show_user_account()

# Page d'inscription
def show_signup_page():
    st.subheader("Créer un nouveau compte")
    email = st.text_input("Email", key="signup_email")
    nom = st.text_input("Nom", key="signup_nom")
    password = st.text_input("Mot de passe", type="password", key="signup_password")

    if st.button("S'inscrire"):
        if email and nom and password:  # Vérifier que tous les champs sont remplis
            try:
                db = next(get_db())  # Initialisation de la connexion DB
                signup_response = signup(db, email, nom, password)
                if signup_response:
                    st.success("Inscription réussie, vous pouvez maintenant vous connecter.")
                    st.session_state['redirect'] = "login"  # Rediriger vers la page de connexion
                    main()  # Re-rendre la page principale
            except HTTPException as e:
                st.error(e.detail)
        else:
            st.error("Veuillez remplir tous les champs avant de vous inscrire.")

# Page de connexion
def show_login_page():
    st.subheader("Se connecter")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Mot de passe", type="password", key="login_password")

    if st.button("Se connecter"):
        if email and password:  # Vérifier que les champs sont remplis
            try:
                db = next(get_db())  # Connexion à la DB
                user = login(db, email, password)
                if user:
                    st.session_state['user'] = user.email
                    st.session_state['nom'] = user.nom
                    st.session_state['logged_in'] = True  # Marquer comme connecté
                    st.session_state['redirect'] = "prediction"  # Rediriger vers la page de prédiction
                    main()  # Re-rendre la page principale
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
        else:
            st.error("Veuillez remplir tous les champs pour vous connecter.")

# Page de prédiction
def show_prediction_page():
    if 'user' not in st.session_state:
        st.error("Vous devez vous connecter pour accéder à cette page.")
        return
    
    st.subheader("Recherche de Véhicule")
    
    # Champ de recherche de véhicule
    kilometrage = st.slider("Kilométrage", 0, 300000, step=1000, key="kilometrage")
    annee = st.slider("Année", 1980, 2024, step=1, key="annee")
    marque = st.selectbox(
    "Marque", 
    [
        "Peugeot", "Renault", "Toyota", "Volkswagen", "Mercedes", "Opel", 
        "Citroën", "Audi", "Suzuki", "Fiat", "Dacia", "BMW", "Tesla", 
        "Nissan", "Ford", "Hyundai", "Cupra", "Kia", "DS", "Seat", 
        "Mini", "BYD", "MG", "Jeep", "Land", "Skoda", "Lynk&Co", 
        "Lexus", "Volvo", "Honda", "Mitsubishi", "Infiniti", 
        "Mazda", "Smart", "Alfa"
    ], 
    key="marque")
    carburant = st.selectbox("Type de Carburant", ["Essence", "Diesel", "Hybride", "Électrique"], key="carburant")
    transmission = st.selectbox("Transmission", ["Manuelle", "Automatique"], key="transmission")
    modele = st.text_input("Modèle", key="modele")
    etat = st.selectbox("État", ["Occasion"], key="etat")

    if st.button("Prédire le Prix"):
        # Appel à l'API FastAPI pour prédiction
        api_url = "http://127.0.0.1:8000/predict_combined"
        payload = {
            "kilometrage": kilometrage,
            "annee": annee,
            "marque": marque,
            "carburant": carburant,
            "transmission": transmission,
            "modele": modele,
            "etat": etat
        }
        # Utiliser le spinner et la barre de progression pendant la prédiction
        with st.spinner('Prédiction en cours...'):
            # Simuler une barre de progression sur 3 secondes
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03)  # Pause de 0.03s pour un total de ~3s
                progress_bar.progress(i + 1)
                
            response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            prediction = response.json().get("predicted_price")
            classification = response.json().get("deal_classification")
            st.success(f"Le prix estimé est de : {prediction:.2f} €")
            st.info(f"Classification de l'offre: {classification}")
            st.balloons()  # Affiche des ballons en guise de succès
        else:
            st.error("Erreur lors de la prédiction")

# Page de compte utilisateur
def show_user_account():
    if 'user' in st.session_state:
        st.subheader(f"Compte de {st.session_state['nom']}")
        st.write(f"Email : {st.session_state['user']}")
        st.write("Historique des recherches à implémenter...")

# Lancer l'application principale
if __name__ == "__main__":
    main()