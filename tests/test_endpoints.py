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
    assert response.status_code == 200 or response.status_code == 201, f"Échec de la création, code d'état: {response.status_code}"
    assert "id" in response.json(), "L'ID du véhicule n'est pas présent dans la réponse"
    return response.json()["id"]

# Test de lecture de tous les véhicules
def test_read_vehicules():
    endpoint = f"{BASE_URL}/vehicules/"
    response = requests.get(endpoint)
    assert response.status_code == 200, f"Échec de la lecture, code d'état: {response.status_code}"
    assert isinstance(response.json(), list), "La réponse n'est pas une liste"

# Test de mise à jour d'un véhicule
def test_update_vehicule():
    vehicule_id = test_create_vehicule()  # Créez un véhicule pour obtenir un ID valide
    endpoint = f"{BASE_URL}/vehicules/{vehicule_id}"
    payload = {
        "modele": "Modèle Mis à Jour",
        "prix": 27000
    }
    response = requests.put(endpoint, json=payload)
    assert response.status_code == 200, f"Échec de la mise à jour, code d'état: {response.status_code}"
    assert response.json()["prix"] == 27000, "Le prix du véhicule n'a pas été mis à jour correctement"

# Test de suppression d'un véhicule
def test_delete_vehicule():
    vehicule_id = test_create_vehicule()  # Créez un véhicule pour obtenir un ID valide
    endpoint = f"{BASE_URL}/vehicules/{vehicule_id}"
    response = requests.delete(endpoint)
    assert response.status_code == 200, f"Échec de la suppression, code d'état: {response.status_code}"
    # Vérifiez que le véhicule a été supprimé
    response = requests.get(endpoint)
    return response.status_code == 404, f"Le véhicule n'a pas été supprimé, code d'état: {response.status_code}"

# Test de création d'un véhicule avec des champs manquants
def test_create_vehicule_missing_fields():
    endpoint = f"{BASE_URL}/vehicules/"
    payload = {
        "modele": "Nouveau Modèle",
        "annee": 2023
        # Manque d'autres champs obligatoires
    }
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 422, f"Échec de la création avec champs manquants, code d'état: {response.status_code}"