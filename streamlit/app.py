# FILE: streamlit/app.py

import os
import sys
from loguru import logger
import streamlit as st
from sqlalchemy.orm import Session

# Ajouter le chemin du dossier parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from API.database import SessionLocal, engine  
from API.models import User  
# Configuration de loguru
logger.add("./streamlit/log/app.log", rotation="500 MB")

# Exemple de journalisation
logger.info("Application démarrée")

st.set_page_config(
    page_title="Prédiction du Prix du Véhicule",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

from streamlit_option_menu import option_menu
from page.connexion import show_signup_page, show_login_page
from page.predict import show_predict_page
from page.home_page import show_home_page
from page.profile_page import show_profile_page  # Importer la fonction pour afficher la page de profil


@st.cache_data
def load_image():
    return os.path.abspath("./streamlit/img/logo.png")


st.image(load_image(), use_container_width=True)

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def show_main_page():
    if st.session_state["logged_in"]:
        db = SessionLocal()
        user = get_user(db, st.session_state["user_id"])
        db.close()

        selected = option_menu(
            menu_title=None,
            options=["Accueil", "Prédiction", f"Hello {user.nom} !", "Déconnexion"],
            icons=["house", "graph-up-arrow", "person", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

        if selected == "Accueil":
            logger.info("Page Accueil sélectionnée")
            show_home_page()
        elif selected == "Prédiction":
            logger.info("Page Prédiction sélectionnée")
            show_predict_page()
        elif selected == f"Hello {user.nom} !":
            show_profile_page()
            logger.info(f"Utilisateur {user.nom} connecté")
        elif selected == "Déconnexion":
            logger.info(f"Utilisateur {user.nom} déconnecté")
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.experimental_user()
    else:
        selected = option_menu(
            menu_title=None,
            options=["Accueil", "Prédiction"],
            icons=["house", "graph-up-arrow"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

        if selected == "Accueil":
            logger.info("Page Accueil sélectionnée")
            show_home_page()
        elif selected == "Prédiction":
            logger.info("Page Prédiction sélectionnée")
            show_predict_page()

# session_state pour gérer l'état de la session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# Affichage de la page appropriée en fonction de l'état de la session
if st.session_state["logged_in"]:
    show_main_page()
elif st.session_state["show_signup"] :
    show_signup_page()
else:
    show_login_page()
