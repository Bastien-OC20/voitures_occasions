import os
import sys
import re
import streamlit as st
import bcrypt
from sqlalchemy.orm import Session

# Ajouter le chemin du dossier parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from API.database import SessionLocal
from API.models import User

# Fonction pour afficher la page de connexion
def show_login_page():
    st.header("Connexion")
    username = st.text_input("Nom d'utilisateur", key="login_username_input")
    password = st.text_input("Mot de passe", type="password", key="login_password_input")
    
    if st.button("Se connecter", key="login_button"):
        user_found = False
        db = SessionLocal()
        user = db.query(User).filter(User.nom == username).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user_found = True
            user_id = user.id  # Extraire l'ID de l'utilisateur avant de fermer la session
            user_nom = user.nom  # Extraire le nom de l'utilisateur avant de fermer la session
        
        db.close()
        
        if user_found:
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id  # Utiliser l'ID extrait
            st.session_state["user_nom"] = user_nom  # Utiliser le nom extrait
            st.session_state["show_signup"] = False
            st.success("Connexion réussie ! Redirection vers la page d'accueil...")
            st.experimental_user()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")
    
    if st.button("S'inscrire", key="signup_redirect_button"):
        st.session_state["show_signup"] = True

# Fonction pour afficher la page d'inscription
def show_signup_page():
    st.header("Inscription")
    new_username = st.text_input("Nom d'utilisateur", key="signup_username_input")
    new_mail = st.text_input("Adresse e-mail", key="signup_email_input")
    new_password = st.text_input(
        "Mot de passe",
        type="password",
        key="signup_password_input",
        placeholder="Minimum 8 caractères, au moins une lettre et un chiffre",
    )

    # Regex 
    username_regex = r'^[a-zA-Z0-9_]{3,20}$'
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$' 

    if st.button("S'inscrire", key="signup_button"):
        if not re.match(username_regex, new_username):
            st.error("Le nom d'utilisateur doit comporter entre 3 et 20 caractères et ne contenir que des lettres, des chiffres et des underscores.")
        elif not re.match(email_regex, new_mail):
            st.error("L'adresse e-mail n'est pas valide.")
        elif not re.match(password_regex, new_password):
            st.error("Le mot de passe doit comporter au moins 8 caractères, dont au moins une lettre et un chiffre.")
        elif new_username and new_mail and new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            db = SessionLocal()
            new_user = User(nom=new_username, email=new_mail, password=hashed_password)
            db.add(new_user)
            db.commit()
            user_id = new_user.id  # Extraire l'ID de l'utilisateur avant de fermer la session
            db.close()
            
            st.success("Inscription réussie ! Redirection vers la page d'accueil...")
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user_id  # Utiliser l'ID extrait
            st.session_state["show_signup"] = False
            st.experimental_user()
        else:
            st.error("Veuillez remplir tous les champs.")

# Fonction pour afficher la page d'accueil
@st.cache_data
def show_home_page():
    st.header("Accueil")
    st.write("Bienvenue sur la page d'accueil !")

# Afficher la page appropriée en fonction de l'état de la session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False

if st.session_state["logged_in"]:
    show_home_page()
elif st.session_state["show_signup"]:
    show_signup_page()
else:
    show_login_page()
