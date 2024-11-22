from pydantic import BaseModel, validator
from typing import Optional

class CarburantBase(BaseModel):
    type: str


class Carburant(CarburantBase):
    id_carburant: int 

    class Config:
        orm_mode = True

class VehiculeBase(BaseModel):
    marque_id: int
    modele: str
    annee: int = validator("annee", pre=True, always=True)(lambda v: v if v > 1900 else ValueError("L'année doit être après 1900"))
    kilometrage: int = validator("kilometrage", pre=True, always=True)(lambda v: f"{v:,}")
    prix: float = validator("prix", pre=True, always=True)(lambda v: f"{v:,.2f}")
    etat: str
    carburant_id: int 
    transmission_id: int 


class VehiculeCreate(VehiculeBase):
    id: int


class VehiculeUpdate(BaseModel):
    marque_id: Optional[int]= None
    modele: Optional[str] = None
    annee: Optional[int] = None
    kilometrage: Optional[int] = None
    prix: Optional[float] = None
    etat: Optional[str] = None
    carburant_id: Optional[int] = None
    transmission_id: Optional[int] = None


class VehiculeDelete(VehiculeBase):
    id: int

class Vehicule(VehiculeBase):
    id: int 
    carburant: Optional[Carburant] = None

    class Config:
        orm_mode = True
