import streamlit as st
import bcrypt
import csv
import re

# Fonction pour afficher la page de connexion
def show_login_page():
    st.header("Connexion")
    username = st.text_input("Nom d'utilisateur", key="login_username_input")
    password = st.text_input("Mot de passe", type="password", key="login_password_input")
    
    if st.button("Se connecter", key="login_button"):
        user_found = False
        with open('./frontend/data/users.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:  # Vérifier que la ligne contient bien trois valeurs
                    stored_username, stored_mail, stored_hashed_password = row
                    if username == stored_username and bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                        user_found = True
                        break
        
        if user_found:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username  # Définir le nom d'utilisateur
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
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            with open('./frontend/data/users.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([new_username, new_mail, hashed_password.decode('utf-8')])
            
            st.success("Inscription réussie ! Redirection vers la page d'accueil...")
            st.session_state["logged_in"] = True
            st.session_state["username"] = new_username  # Définir le nom d'utilisateur
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
