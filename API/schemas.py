from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CarburantBase(BaseModel):
    type: str

class CarburantCreate(CarburantBase):
    pass

class Carburant(CarburantBase):
    id_carburant: int

    class Config:
        orm_mode = True

class TransmissionBase(BaseModel):
    type: str

class TransmissionCreate(TransmissionBase):
    pass

class Transmission(TransmissionBase):
    id_transmission: int

    class Config:
        orm_mode = True

class MarqueBase(BaseModel):
    nom: str

class MarqueCreate(MarqueBase):
    pass

class Marque(MarqueBase):
    id_marque: int

    class Config:
        orm_mode = True

class VehiculeBase(BaseModel):
    marque_id: int
    modele: str
    annee: int = Field(..., ge=1950, le=datetime.now().year)
    kilometrage: int = Field(..., ge=0)
    prix: float = Field(..., ge=0)
    etat: str
    carburant_id: int
    transmission_id: int

class VehiculeCreate(VehiculeBase):
    pass

class PredictRequest(BaseModel):
    kilometrage: float
    annee: int
    marque: str
    carburant: str
    transmission: str

    class Config:
        schema_extra = {
            "example": {
                "kilometrage": 15000,
                "annee": 2019,
                "marque": "Peugeot",
                "carburant": "Essence",
                "transmission": "Manuelle"
            }
        }

class VehiculeUpdate(BaseModel):
    marque_id: Optional[int] = None
    modele: Optional[str] = None
    annee: Optional[int] = None
    kilometrage: Optional[int] = None
    prix: Optional[float] = None
    etat: Optional[str] = None
    carburant_id: Optional[int] = None
    transmission_id: Optional[int] = None

class Vehicule(VehiculeBase):
    id: int
    carburant: Optional[Carburant] = None
    transmission: Optional[Transmission] = None

    class Config:
        orm_mode = True