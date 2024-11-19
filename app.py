from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

# Initialiser le driver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # Pour essayer de contourner les détections automatiques
options.add_argument("--headless")  # Exécute Chrome en mode headless pour plus de discrétion
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

voitures = []

# Scraper chaque page
for current_page in range(1, 101):
    try:
        # Naviguer vers l'URL de la page actuelle
        url = f"https://www.aramisauto.com/achat/occasion?page={current_page}"
        driver.get(url)

        # Attendre le chargement de la page
        time.sleep(3)

        print(f"Scraping page {current_page}")
        
        # Trouver tous les conteneurs des annonces
        annonces = driver.find_elements(By.CLASS_NAME, "item")

        # Extraire les informations de chaque annonce
        for annonce in annonces:
            try:
                # Extraire la marque et le modèle
                marque_modele = annonce.find_element(By.CLASS_NAME, 'product-card-vehicle-information__title').text

                # Extraire le prix
                prix = annonce.find_element(By.CLASS_NAME, 'heading-l').text

                # Extraire les autres informations (année, kilométrage, type de carburant)
                details_brut = annonce.find_element(By.CLASS_NAME, 'product-card-vehicle-information__bottom').text

                # Diviser les détails en fonction des séparateurs visuels (ici "•")
                details = details_brut.split("\u2022")

                # Nettoyer les espaces superflus
                details = [detail.strip() for detail in details]

                # Extraire chaque information (en vérifiant la longueur de la liste)
                annee = details[0] if len(details) > 0 else "Non spécifié"
                kilometrage = details[1] if len(details) > 1 else "Non spécifié"
                etat = details[2] if len(details) > 2 else "Non spécifié"

                voitures.append({
                    'Marque/Modèle': marque_modele,
                    'Année': annee,
                    'Kilométrage': kilometrage,
                    'Etat': etat,
                    'Prix': prix
                })
            except Exception as e:
                print(f"Erreur lors de l'extraction: {e}")
    except Exception as e:
        print(f"Erreur lors de la pagination: {e}")
        break

# Créer un DataFrame et sauvegarder dans un fichier CSV
df = pd.DataFrame(voitures)
df.to_csv('voitures_aramisauto.csv', index=False)

# Fermer le driver
driver.quit()