from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from . import models, schemas

# Fonction pour obtenir la liste des véhicules
def get_vehicules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Vehicule).offset(skip).limit(limit).all()

# Fonction pour créer un nouveau véhicule
def create_vehicule(db: Session, vehicule: schemas.VehiculeCreate):
    db_vehicule = models.Vehicule(**vehicule.dict())
    db.add(db_vehicule)
    db.commit()
    db.refresh(db_vehicule)
    return db_vehicule

# Fonction pour mettre à jour un véhicule
def update_vehicule(db: Session, vehicule_id: int, vehicule_update: schemas.VehiculeUpdate):
    db_vehicule = db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()
    if not db_vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    update_data = vehicule_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vehicule, key, value)
    db.commit()
    db.refresh(db_vehicule)
    return db_vehicule

# Fonction pour supprimer un véhicule
def delete_vehicule(db: Session, vehicule_id: int):
    try:
        # Rechercher le véhicule à supprimer
        db_vehicule = db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()
        
        if not db_vehicule:
            raise HTTPException(status_code=404, detail="Véhicule non trouvé")

        # Supprimer le véhicule
        db.delete(db_vehicule)
        db.commit()

        # Retourner un simple message de confirmation
        return {"message": f"Véhicule avec ID {vehicule_id} supprimé avec succès"}

    except Exception as e:
        db.rollback()  # Annuler la transaction en cas d'erreur
        raise HTTPException(status_code=500, detail=f"Erreur serveur lors de la suppression du véhicule: {str(e)}")