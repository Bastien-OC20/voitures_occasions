import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

# Test de création d'un véhicule
def test_create_vehicule():
    endpoint = f"{BASE_URL}/vehicules/"
    payload = {
        "marque_id": 1,
        "modele": "Nouveau Modèle",
        "annee": 2023,
        "kilometrage": 1000,
        "prix": 25000,
        "etat": "Occasion",
        "carburant_id": 1,
        "transmission_id": 1
    }
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200 or response.status_code == 201
    assert "id" in response.json()

# Test de lecture de tous les véhicules
def test_read_vehicules():
    endpoint = f"{BASE_URL}/vehicules/"
    response = requests.get(endpoint)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test de mise à jour d'un véhicule
def test_update_vehicule():
    vehicule_id = 2312  # Remplacer par un ID valide existant
    endpoint = f"{BASE_URL}/vehicules/{vehicule_id}"
    payload = {
        "modele": "Modèle Mis à Jour",
        "prix": 27000
    }
    response = requests.put(endpoint, json=payload)
    assert response.status_code == 200
    assert response.json()["prix"] == 27000

# Test de suppression d'un véhicule
def test_delete_vehicule():
    vehicule_id = 2302  # Remplacer par un ID valide existant
    endpoint = f"{BASE_URL}/vehicules/{vehicule_id}"
    
    # Vérifier que le véhicule existe avant la suppression
    response_get = requests.get(endpoint)
    if response_get.status_code == 404:
        pytest.skip(f"Le véhicule avec l'ID {vehicule_id} n'existe pas, impossible de tester la suppression.")
    
    # Effectuer la suppression
    response_delete = requests.delete(endpoint)
    assert response_delete.status_code == 200, f"Échec de la suppression, code d'état: {response_delete.status_code}"
    
    # Vérifier le message de confirmation
    response_data = response_delete.json()
    assert "message" in response_data, "La réponse ne contient pas de message"
    assert response_data["message"] == f"Véhicule avec ID {vehicule_id} supprimé avec succès"
    
    # Vérifier que le véhicule n'existe plus après la suppression
    response_get_after = requests.get(endpoint)
    assert response_get_after.status_code in [404, 405], "Le véhicule existe toujours après la suppression ou la méthode n'est pas autorisée"

# Test de création d'un véhicule avec des champs manquants
def test_create_vehicule_missing_fields():
    endpoint = f"{BASE_URL}/vehicules/"
    payload = {
        "modele": "Nouveau Modèle",
        "annee": 2023
        # Manque d'autres champs obligatoires
    }
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 422  # Code HTTP pour une requête malformée (champs obligatoires manquants)