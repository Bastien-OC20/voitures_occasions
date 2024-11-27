from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from API import models, schemas, crud
from API.database import SessionLocal, engine
import joblib
import pandas as pd
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Configurer CORS
origins = [
    "http://localhost:8000",
    "http://localhost:8501",  
    "http://127.0.0.1:8501",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dépendance pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Charger les modèles nécessaires
random_forest_model = joblib.load("./models/random_forest_model.pkl")
logistic_regression_model = joblib.load("./models/logistic_regression_model.pkl")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de prédiction de prix de voitures"}

@app.get("/vehicules/", response_model=list[schemas.Vehicule])
def read_vehicules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_vehicules(db, skip=skip, limit=limit)

@app.post("/vehicules/", response_model=schemas.Vehicule, status_code=201)
def create_vehicule(vehicule: schemas.VehiculeCreate, db: Session = Depends(get_db)):
    return crud.create_vehicule(db=db, vehicule=vehicule)

@app.put("/vehicules/{vehicule_id}", response_model=schemas.Vehicule)
def update_vehicule(vehicule_id: int, vehicule_update: schemas.VehiculeUpdate, db: Session = Depends(get_db)):
    db_vehicule = crud.update_vehicule(db=db, vehicule_id=vehicule_id, vehicule_update=vehicule_update)
    if db_vehicule is None:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    return db_vehicule

@app.delete("/vehicules/{vehicule_id}", response_model=dict)
def delete_vehicule(vehicule_id: int, db: Session = Depends(get_db)):
    return crud.delete_vehicule(db=db, vehicule_id=vehicule_id)


@app.post("/predict")
def predict(request: schemas.PredictRequest):
    try:
        # Convertir les données de la requête en DataFrame
        input_data = pd.DataFrame([request.model_dump()])
        logging.info(f"Input data: {input_data}")

        # Renommer les colonnes pour correspondre à celles utilisées lors de l'entraînement
        input_data = input_data.rename(
            columns={
                "kilometrage": "Kilométrage",
                "annee": "Année",
                "marque": "Marque",
                "carburant": "Type de Carburant",
                "transmission": "Transmission",
                "modele": "Modèle",
                "etat": "Etat",
            }
        )
        logging.info(f"Input data with correct column names: {input_data}")

        # Faire la prédiction directement avec le modèle Random Forest
        rf_prediction = random_forest_model.predict(input_data)[0]
        logging.info(f"Random Forest prediction: {rf_prediction}")

        # Faire la prédiction directement avec le modèle de régression logistique
        lr_prediction = logistic_regression_model.predict(input_data)[0]
        logging.info(f"Logistic Regression prediction: {lr_prediction}")

        # Déterminer si le prix est bon ou mauvais
        price_evaluation = "Bon prix" if lr_prediction == 1 else "Mauvais prix"

        return {
            "random_forest_prediction": float(rf_prediction),
            "logistic_regression_evaluation": price_evaluation,
        }

    except Exception as e:
        logging.error(f"Erreur lors de la prédiction: {e}")
        raise HTTPException(status_code=400, detail="Erreur lors de la prédiction")
