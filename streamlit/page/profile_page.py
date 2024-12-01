import os
import sys
import streamlit as st
from datetime import datetime
from sqlalchemy.orm import Session

# Ajouter le chemin du dossier parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from API.database import SessionLocal
from API.models import User

def get_user_info(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user

def update_user_info(user_id, username, email, profile_image=None):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.nom = username
        user.email = email
        if profile_image:
            user.profile_image = profile_image
        db.commit()
    db.close()

def delete_user(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()

def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

def show_profile_page():
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("Utilisateur non connecté.")
        return

    user = get_user_info(user_id)
    if not user:
        st.error("Utilisateur non trouvé.")
        return

    st.title(f"Bienvenue, {user.nom} !")
    
    if "login_time" not in st.session_state:
        st.session_state["login_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Heure de connexion : {st.session_state['login_time']}")

    # Afficher l'image de profil actuelle
    st.subheader("Image de profil")
    if user.profile_image:
        st.image(user.profile_image, width=150)
    else:
        st.write("Aucune image de profil disponible.")

    # Permettre le téléchargement d'une nouvelle image de profil
    uploaded_file = st.file_uploader("Télécharger une nouvelle image de profil", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        profile_image_path = os.path.join("./streamlit/img/profile_images", f"profile_{user_id}.png")
        with open(profile_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Image de profil téléchargée avec succès.")
        update_user_info(user_id, user.nom, user.email, profile_image_path)
        user.profile_image = profile_image_path

    # Afficher les informations de profil actuelles
    st.subheader("Informations de profil")
    username = st.text_input("Nom d'utilisateur", user.nom)
    email = st.text_input("Adresse e-mail", user.email)

    if st.button("Enregistrer les modifications"):
        update_user_info(user_id, username, email, user.profile_image)
        st.session_state["username"] = username
        st.session_state["email"] = email
        st.success("Les informations de profil ont été mises à jour.")

    # Bouton pour supprimer le compte
    if st.button("Supprimer mon compte"):
        delete_user(user_id)
        st.session_state.clear()
        st.success("Votre compte a été supprimé.")
        st.experimental_rerun()

    # Si l'utilisateur est un super utilisateur, afficher les autres utilisateurs
    if user.is_superuser:
        st.subheader("Liste des utilisateurs")
        users = get_all_users()
        for u in users:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(f"Nom: {u.nom}")
            with col2:
                st.write(f"Email: {u.email}")
            with col3:
                if st.button(f"Supprimer {u.nom}", key=u.id):
                    delete_user(u.id)
                    st.success(f"Le compte de {u.nom} a été supprimé.")
                    st.experimental_rerun()

# Afficher la page de profil
show_profile_page()
