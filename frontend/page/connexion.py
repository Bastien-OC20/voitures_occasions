import streamlit as st
import bcrypt
import csv

# Fonction pour afficher la page de connexion
def show_login_page():
    st.header("Connexion")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
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
            st.session_state["show_signup"] = False
            st.success("Connexion réussie ! Redirection vers la page d'accueil...")
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect")
    
    if st.button("S'inscrire"):
        st.session_state["show_signup"] = True

# Fonction pour afficher la page d'inscription
def show_signup_page():
    st.header("Inscription")
    new_username = st.text_input("Nom d'utilisateur", key="signup_username")
    new_mail = st.text_input("Adresse e-mail", key="signup_email")
    new_password = st.text_input("Mot de passe", type="password", key="signup_password")
    
    if st.button("S'inscrire"):
        if new_username and new_mail and new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            with open('./frontend/data/users.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([new_username, new_mail, hashed_password.decode('utf-8')])
            
            st.success("Inscription réussie ! Redirection vers la page d'accueil...")
            st.session_state["logged_in"] = True
            st.session_state["show_signup"] = False
        else:
            st.error("Veuillez remplir tous les champs.")

# Fonction pour afficher la page d'accueil
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
