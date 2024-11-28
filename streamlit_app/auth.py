import streamlit as st
from API.models import User 
from API import database
from sqlalchemy.orm import Session
import bcrypt
from pydantic import BaseModel
from fastapi import HTTPException

# Connexion à la base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schéma Pydantic pour l'inscription
class UserCreate(BaseModel):
    email: str
    nom: str
    password: str

# Fonction d'inscription
def signup(db: Session, email: str, nom: str, password: str):
    # Vérifier si l'utilisateur existe déjà
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    # Hashage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Créer un nouvel utilisateur
    new_user = User(email=email, nom=nom, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Inscription réussie", "user": {"email": new_user.email, "nom": new_user.nom}}

# Connexion de l'utilisateur
def login(db: Session, email: str, password: str):
    # Rechercher l'utilisateur par email
    user = db.query(User).filter(User.email == email).first()

    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    else:
        st.error("Email ou mot de passe incorrect.")
        return None