from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from . import models, schemas

# Fonction pour obtenir la liste des véhicules
def get_vehicules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Vehicule).offset(skip).limit(limit).all()

# Fonction pour créer un nouveau véhicule
def create_vehicule(db: Session, vehicule: schemas.VehiculeCreate):
    db_vehicule = models.Vehicule(**vehicule.model_dump())
    db.add(db_vehicule)
    db.commit()
    db.refresh(db_vehicule)
    return db_vehicule

# Fonction pour mettre à jour un véhicule
def update_vehicule(db: Session, vehicule_id: int, vehicule_update: schemas.VehiculeUpdate):
    db_vehicule = db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()
    if not db_vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    update_data = vehicule_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vehicule, key, value)
    db.commit()
    db.refresh(db_vehicule)
    return db_vehicule


# Fonction pour supprimer un véhicule
def delete_vehicule(db: Session, vehicule_id: int):
    vehicule = (
        db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()
    )
    if vehicule is None:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    db.delete(vehicule)
    db.commit()
    return {"message": "Véhicule supprimé avec succès"}
