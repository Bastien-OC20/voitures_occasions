# FILE: front/app.py

import streamlit as st
from streamlit_option_menu import option_menu
from page.connexion import show_signup_page, show_login_page
from page.predict import show_predict_page

st.set_page_config(page_title="Prédiction du Prix du Véhicule", page_icon="🚗") 


def show_main_page(): 
    st.header("Prédiction du Prix du Véhicule")  
 
    
    selected = option_menu(
        menu_title=None,
        options=["Accueil", "Prédiction"],
        icons=["house", "graph-up-arrow"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"  
    )
    
  
    if selected == "Accueil":
        st.header("Bienvenue sur le site de prédiction du Prix du Véhicule")
        st.write("Utilisez le menu pour naviguer vers la page de prédiction.") 
    elif selected == "Prédiction":  
        show_predict_page()  
 

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False  

if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False 

if st.session_state["logged_in"]: 
    show_main_page()
elif st.session_state["show_signup"]: 
    show_signup_page()  
else:  
    show_login_page() 
