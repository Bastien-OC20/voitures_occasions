import streamlit as st
from datetime import datetime

def show_profile_page():
    st.title(f"Bienvenue, {st.session_state['username']} !")
    
    
    if "login_time" not in st.session_state:
        st.session_state["login_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"Heure de connexion : {st.session_state['login_time']}")


    def download_report(report_name):
        with open(report_name, "rb") as file:
            btn = st.download_button(
                label=f"Télécharger {report_name}",
                data=file,
                file_name=report_name,
                mime="text/plain"
            )
        return btn


    if "reports" in st.session_state:
        st.write("Télécharger les rapports de prédiction :")
        for report in st.session_state["reports"]:
            download_report(report)
    else:
        st.write("Aucun rapport de prédiction disponible.")
