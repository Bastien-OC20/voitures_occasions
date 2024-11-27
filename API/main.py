from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Depends
from . import models, schema, crud
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/vehicules/", response_model=schema.Vehicule)
def read_vehicules(db: Session = Depends(get_db)):
    return crud.get_vehicule(db)

@app.post("/vehicules/", response_model=schema.Vehicule)
def create_vehicules(db: Session = Depends(get_db)):
    return crud.create_vehicule(db)

@app.put("/vehicules/{vehicule_id}", response_model=schema.Vehicule)
def update_vehicules(db:Session= Depends(get_db)):
    return crud.update_vehicule(db)

@app.delete("/vehicules/{vehicule_id}", response_model=schema.Vehicule)
def delete_vehicule(db:Session= Depends(get_db)):
    return crud.delete_vehicule(db)