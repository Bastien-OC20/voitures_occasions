# from schema import VehiculeCreate, VehiculeUpdate
from sqlalchemy.orm import Session
from . import models, schema


# # Fonction pour obtenir la liste des véhicules
# def get_vehicule(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(models.Vehicule).offset(skip).limit(limit).all()


# # Fonction pour créer un nouveau véhicule
# def create_vehicule(db: Session, vehicule: schema.VehiculeCreate):
#     db_vehicule = models.Vehicule(**vehicule.dict())
#     db.add(db_vehicule)
#     db.commit()
#     db.refresh(db_vehicule)
#     return db_vehicule


# # Fonction pour mettre à jour un véhicule
# def update_vehicule(
#     db: Session, ID_vehicule: int, vehicule_update: schema.VehiculeUpdate
# ):
#     db_vehicule = db.query(models.Vehicule).filter(ID_vehicule == ID_vehicule).first()
#     if not db_vehicule:
#         return None
#     for key, value in vehicule_update.dict(exclude_unset=True).items():
#         setattr(db_vehicule, key, value)
#     db.commit()
#     db.refresh(db_vehicule)
#     return db_vehicule


# # Fonction pour supprimer un véhicule
# def delete_vehicule(db: Session, ID_vehicule: int):
#     db_vehicule = db.query(models.Vehicule).filter(models.Vehicule.ID_vehicule == ID_vehicule).first()
#     if db_vehicule:
#         db.delete(db_vehicule)
#         db.commit()
#     return db_vehicule


# Fonction pour obtenir la liste des véhicules
def get_vehicules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Vehicule).offset(skip).limit(limit).all()


# Fonction pour créer un nouveau véhicule
def create_vehicule(db: Session, vehicule: schema.VehiculeCreate):
    db_vehicule = models.Vehicule(**vehicule.dict())
    db.add(db_vehicule)
    db.commit()
    db.refresh(db_vehicule)
    return db_vehicule


# Fonction pour mettre à jour un véhicule
def update_vehicule(
    db: Session, vehicule_id: int, vehicule_update: schema.VehiculeUpdate
):
    db_vehicule = (
        db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()
    )
    if not db_vehicule:
        return None
    for key, value in vehicule_update.dict(exclude_unset=True).items():
        setattr(db_vehicule, key, value)
    db.commit()
    db.refresh(db_vehicule)
    return db_vehicule


# Fonction pour supprimer un véhicule
def delete_vehicule(db: Session, vehicule_id: int):
    db_vehicule = (
        db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()
    )
    if db_vehicule:
        db.delete(db_vehicule)
        db.commit()
    return db_vehicule
