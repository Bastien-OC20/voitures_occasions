from sqlalchemy.orm import Session
from fastapi import HTTPException
from API import models, schemas

# Fonction pour obtenir la liste des véhicules
def get_vehicules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Vehicule).offset(skip).limit(limit).all()

# Fonction pour obtenir un véhicule par ID
def get_vehicule(db: Session, vehicule_id: int):
    vehicule = db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()
    if not vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    return vehicule

# Fonction pour créer un véhicule
def create_vehicule(db: Session, vehicule: schemas.VehiculeCreate):
    db_vehicule = models.Vehicule(
        annee=vehicule.annee,
        kilometrage=vehicule.kilometrage,
        prix=vehicule.prix,
        etat=vehicule.etat,
        marque_id=vehicule.marque_id,
        modele_id=vehicule.modele_id,
        carburant_id=vehicule.carburant_id,
        transmission_id=vehicule.transmission_id,
    )
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
    db_vehicule = db.query(models.Vehicule).filter(models.Vehicule.id == vehicule_id).first()
    if not db_vehicule:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    db.delete(db_vehicule)
    db.commit()
    return {"message": "Véhicule supprimé avec succès"}

# Fonction pour obtenir la liste des utilisateurs
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# Fonction pour obtenir un utilisateur par ID
def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

# Fonction pour créer un utilisateur
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        nom=user.nom,
        password=user.password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        profile_image=user.profile_image,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Fonction pour mettre à jour un utilisateur
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# Fonction pour supprimer un utilisateur
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db.delete(db_user)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès"}
