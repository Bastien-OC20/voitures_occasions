from fastapi import FastAPI, HTTPException, Depends
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

# Dépendance pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Charger les modèles nécessaires
random_forest_model = joblib.load("./models/random_forest_model.pkl")
logistic_model = joblib.load("./models/logistic_regression_model.pkl")

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

class PredictRequest(BaseModel):
    kilometrage: float
    annee: int
    marque: str
    carburant: str
    transmission: str
    modele: str
    etat: str

    class Config:
        schema_extra = {
            "example": {
                "kilometrage": 15000,
                "annee": 2019,
                "marque": "Peugeot",
                "carburant": "Essence",
                "transmission": "Manuelle",
                "modele": "208",
                "etat": "Occasion"
            }
        }

# @app.post("/predict_random_forest")
# def predict_random_forest(request: PredictRequest):
#     try:
#         # Convertir les données de la requête en DataFrame
#         input_data = pd.DataFrame([request.dict()])
#         logging.info(f"Input data: {input_data}")

#         # S'assurer que les colonnes correspondent aux colonnes utilisées lors de l'entraînement
#         column_order = [
#             'Kilométrage', 'Année', 'Marque', 'Type de Carburant', 
#             'Transmission', 'Modèle', 'Etat'
#         ]
        
#         # Adapter les noms des colonnes à ceux du modèle
#         input_data.columns = column_order
#         logging.info(f"Input data with correct columns: {input_data}")

#         # Faire la prédiction directement avec le modèle
#         prediction = random_forest_model.predict(input_data)
#         return {"prediction": float(prediction[0])}
    
#     except Exception as e:
#         logging.error(f"Erreur lors de la prédiction: {e}")
#         raise HTTPException(status_code=400, detail="Erreur lors de la prédiction")
    
    
@app.post("/predict_combined")
def predict_combined(request: PredictRequest):
    try:
        # Convertir les données de la requête en DataFrame
        input_data = pd.DataFrame([request.dict()])
        logging.info(f"Input data: {input_data}")

        # S'assurer que les colonnes correspondent aux colonnes utilisées lors de l'entraînement
        column_order = [
            'Kilométrage', 'Année', 'Marque', 'Type de Carburant', 
            'Transmission', 'Modèle', 'Etat'
        ]

        # Adapter les noms des colonnes à ceux du modèle
        input_data.columns = column_order
        logging.info(f"Input data with correct columns: {input_data}")

        # Prédiction du prix avec le modèle Random Forest
        predicted_price = random_forest_model.predict(input_data)
        logging.info(f"Predicted price: {predicted_price}")

        # Classification de la transaction (Bonne ou Mauvaise affaire) avec le modèle Logistique
        deal_classification = logistic_model.predict(input_data)
        label = "Bonne affaire" if deal_classification[0] == 1 else "Mauvaise affaire"
        logging.info(f"Classification: {label}")

        # Retourner les deux prédictions
        return {
            "predicted_price": float(predicted_price[0]),
            "deal_classification": label
        }
    
    except Exception as e:
        logging.error(f"Erreur lors de la prédiction combinée: {e}")
        raise HTTPException(status_code=400, detail="Erreur lors de la prédiction combinée")
