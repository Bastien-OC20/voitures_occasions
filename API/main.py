# from fastapi import FastAPI, Depends, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from .database import SessionLocal
# from .crud import get_vehicule, create_vehicule, update_vehicule, delete_vehicule
# # from schema import VehiculeCreate, VehiculeUpdate, VehiculeDelete, VehiculeBase
# from API import models, schema, crud


# app = FastAPI(title="Gestion des véhicules", version="1.0")


# origins = [
#     "http://localhost:8501",  # frontend en en streamlit
#     "http://127.0.0.1:8000",  # Backend en local de FastAPI
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/vehicules/", response_model=list[schema.Vehicule])
# def read_vehicules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return crud.get_vehicule(db, skip=skip, limit=limit)


# @app.post("/vehicules/", response_model=schema.Vehicule)
# def create_new_vehicule(vehicule: schema.VehiculeCreate, db: Session = Depends(get_db)):
#     return crud.create_vehicule(db, vehicule)


# @app.put("/vehicules/{vehicule_id}", response_model=schema.Vehicule)
# def update_vehicule(
#     vehicule_id: int, vehicule: schema.VehiculeUpdate, db: Session = Depends(get_db)
# ):
#     updated_vehicule = crud.update_vehicule(db, vehicule_id, vehicule)
#     if updated_vehicule is None:
#         raise HTTPException(status_code=404, detail="Véhicule introuvable")
#     return updated_vehicule


# @app.delete("/vehicules/{vehicule_id}", response_model=schema.Vehicule)
# def delete_vehicule(
#     vehicule_id: int, db: Session = Depends(get_db)
# ):
#     deleted_vehicule = crud.delete_vehicule(db, vehicule_id)
#     if deleted_vehicule is None:
#         raise HTTPException(status_code=404, detail="Véhicule introuvable")
#     return {"message": "Véhicule supprimé avec succès"}


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from API import models, schema, crud
from API.database import SessionLocal, engine

# # Créer les tables dans la base de données
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dépendance pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/vehicules/", response_model=list[schema.Vehicule])
def read_vehicules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_vehicules(db, skip=skip, limit=limit)


@app.post("/vehicules/", response_model=schema.Vehicule)
def create_vehicule(vehicule: schema.VehiculeCreate, db: Session = Depends(get_db)):
    return crud.create_vehicule(db=db, vehicule=vehicule)


@app.put("/vehicules/{vehicule_id}", response_model=schema.Vehicule)
def update_vehicule(
    vehicule_id: int,
    vehicule_update: schema.VehiculeUpdate,
    db: Session = Depends(get_db),
):
    db_vehicule = crud.update_vehicule(
        db=db, vehicule_id=vehicule_id, vehicule_update=vehicule_update
    )
    if db_vehicule is None:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    return db_vehicule


@app.delete("/vehicules/{vehicule_id}", response_model=schema.Vehicule)
def delete_vehicule(vehicule_id: int, db: Session = Depends(get_db)):
    db_vehicule = crud.delete_vehicule(db=db, vehicule_id=vehicule_id)
    if db_vehicule is None:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    return db_vehicule
