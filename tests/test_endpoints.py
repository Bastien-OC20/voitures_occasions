import requests
import sys
import os
import uuid
from sqlalchemy.orm import Session
import pytest

# Ajouter le chemin du dossier parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from API.database import SessionLocal
from API.models import User

BASE_URL = "http://127.0.0.1:8000"

# Fixture pour créer un véhicule et fournir son ID
@pytest.fixture(scope="module")
def vehicule_cree():
    endpoint = f"{BASE_URL}/vehicules/"
    payload = {
        "marque_id": 1,
        "modele_id": 1,
        "annee": 2023,
        "kilometrage": 1000,
        "prix": 25000,
        "etat": "Occasion",
        "carburant_id": 1,
        "transmission_id": 1
    }
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 201, f"Échec de la création du véhicule, code d'état: {response.status_code}, réponse: {response.text}"
    assert "id" in response.json(), "L'ID du véhicule n'est pas présent dans la réponse"
    vehicule_id = response.json()["id"]
    yield vehicule_id
    # Code pour le nettoyage après les tests (suppression du véhicule)
    endpoint_delete = f"{BASE_URL}/vehicules/{vehicule_id}"
    requests.delete(endpoint_delete)

def test_read_vehicules():
    endpoint = f"{BASE_URL}/vehicules/"
    response = requests.get(endpoint)
    assert response.status_code == 200, f"Échec de la lecture, code d'état: {response.status_code}, réponse: {response.text}"
    assert isinstance(response.json(), list), "La réponse n'est pas une liste"

def test_update_vehicule(vehicule_cree):
    endpoint = f"{BASE_URL}/vehicules/{vehicule_cree}"
    payload = {
        "modele_id": 2,
        "annee": 2024,
        "kilometrage": 500,
        "prix": 26000,
        "etat": "Neuf"
    }
    response = requests.put(endpoint, json=payload)
    assert response.status_code == 200, f"Échec de la mise à jour, code d'état: {response.status_code}, réponse: {response.text}"
    updated_vehicule = response.json()
    assert updated_vehicule["modele_id"] == 2, "Le modèle n'a pas été mis à jour"

def test_delete_vehicule(vehicule_cree):
    endpoint = f"{BASE_URL}/vehicules/{vehicule_cree}"
    response = requests.delete(endpoint)
    assert response.status_code == 200, f"Échec de la suppression, code d'état: {response.status_code}, réponse: {response.text}"
    assert response.json()["message"] == "Véhicule supprimé avec succès", "Le message de suppression n'est pas correct"

# Test de création d'un utilisateur
@pytest.fixture
def test_create_user():
    endpoint = f"{BASE_URL}/users/"
    unique_email = f"user_{uuid.uuid4()}@example.com"
    payload = {
        "email": unique_email,
        "nom": "user",
        "is_active": True,
        "is_superuser": False,
        "profile_image": None,
        "password": "baballe13"
    }
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200, f"Échec de la création, code d'état: {response.status_code}, réponse: {response.text}"
    assert "id" in response.json(), "L'ID de l'utilisateur n'est pas présent dans la réponse"
    return response.json()["id"]


# Test de lecture de tous les utilisateurs
@pytest.fixture
def test_read_users():
    endpoint = f"{BASE_URL}/users/"
    response = requests.get(endpoint)
    assert response.status_code == 200, f"Échec de la création, code d'état: {response.status_code}, réponse: {response.text}"
    assert isinstance(response.json(), list), "La réponse n'est pas une liste"


# Test de mise à jour d'un utilisateur
@pytest.fixture
def test_update_user():
    user_id = test_create_user()  # Créez un utilisateur pour obtenir un ID valide
    endpoint = f"{BASE_URL}/users/{user_id}"
    unique_email = f"updated_user_{uuid.uuid4()}@example.com"
    payload = {
        "email": unique_email,
        "nom": "Sebastien",
        "is_active": True,
        "is_superuser": True,
        "profile_image": None
    }
    response = requests.put(endpoint, json=payload)
    assert response.status_code == 200, f"Échec de la mise à jour, code d'état: {response.status_code}, réponse: {response.text}"
    updated_user = response.json()
    assert updated_user["nom"] == "Sebastien", "Le nom n'a pas été mis à jour"
    assert updated_user["email"] == unique_email, "L'email n'a pas été mis à jour"
    assert updated_user["is_active"], "Le statut actif n'a pas été mis à jour"
    assert updated_user["is_superuser"], "Le statut super utilisateur n'a pas été mis à jour"


# Test de suppression d'un utilisateur
@pytest.fixture
def test_delete_user():
    user_id = test_create_user()  # Créez un utilisateur pour obtenir un ID valide
    endpoint = f"{BASE_URL}/users/{user_id}"
    response = requests.delete(endpoint)
    assert response.status_code == 200, f"Échec de la suppression, code d'état: {response.status_code}, réponse: {response.text}"
    assert response.json()["message"] == "Utilisateur supprimé avec succès", "Le message de suppression n'est pas correct"


@pytest.fixture
def test_create_and_update_user():
    # Création de l'utilisateur
    endpoint_create = f"{BASE_URL}/users/"
    unique_email = f"user_{uuid.uuid4()}@example.com"
    payload_create = {
        "email": unique_email,
        "nom": "user",
        "is_active": True,
        "is_superuser": False,
        "profile_image": None,
        "password": "password123"
    }
    response_create = requests.post(endpoint_create, json=payload_create)
    assert response_create.status_code == 200, f"Échec de la création, code d'état: {response_create.status_code}, réponse: {response_create.text}"
    user_id = response_create.json()["id"]

    # Mise à jour de l'utilisateur
    endpoint_update = f"{BASE_URL}/users/{user_id}"
    updated_email = f"user_{uuid.uuid4()}@example.com"
    payload_update = {
        "email": updated_email,
        "nom": "updated_user",
        "is_active": True,
        "is_superuser": True,
        "profile_image": None
    }
    response_update = requests.put(endpoint_update, json=payload_update)
    assert response_update.status_code == 200, f"Échec de la mise à jour, code d'état: {response_update.status_code}, réponse: {response_update.text}"
    updated_user = response_update.json()
    assert updated_user["email"] == updated_email, "L'email n'a pas été mis à jour"

# Exécuter les tests
if __name__ == "__main__":
    test_read_vehicules()
    test_update_vehicule()
    test_delete_vehicule()
    test_create_user()
    test_read_users()
    test_update_user()
    test_delete_user()
    test_create_and_update_user()
