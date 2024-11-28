
# **Gestion des Voitures - Analyse et Modélisation des Prix**

Ce projet vise à analyser les caractéristiques des voitures d'occasion et à prédire leur prix à l'aide de modèles de machine learning, notamment **Random Forest** et **régression logistique**. Ce document fournit un aperçu des objectifs, de la structure et des outils utilisés dans le projet.

---

## **Objectifs**

1. **Analyse des données** :
   - Explorer les facteurs influençant le prix des voitures (kilométrage, année, carburant, etc.).
   - Identifier les relations entre les variables.

2. **Modélisation prédictive** :
   - Développer un modèle capable de prédire si une voiture coûte plus ou moins que la médiane des prix (classification binaire).
   - Tester plusieurs algorithmes et optimiser leurs performances.

---

## **Technologies et Bibliothèques**

### **Langages et Frameworks**

- **Python** : Langage principal utilisé pour le traitement des données et la modélisation.

### **Bibliothèques principales**

- **Pandas** : Manipulation des données.
- **Scikit-learn** : Prétraitement, modèles machine learning (Random Forest et régression logistique), et évaluation.
- **Matplotlib / Seaborn** : Visualisation des données.
- **StandardScaler** : Standardisation des variables numériques.

---

## **Structure du Projet**

### **Fichiers**

- `voitures_aramisauto_nettoye.csv` : Jeu de données nettoyé contenant les caractéristiques des voitures.
- `main.py` : Script principal pour le traitement des données, l'entraînement des modèles et l'évaluation.
- `README.md` : Documentation complète du projet.

### **Étapes Principales**

1. **Chargement des Données** :
   - Lecture et nettoyage du fichier CSV.
   - Transformation des variables catégorielles en numériques (encodage One-Hot).

2. **Création des Variables** :
   - Ajout d'une variable binaire (`Prix_binaire`) indiquant si le prix est supérieur à la médiane.

3. **Standardisation** :
   - Mise à l'échelle des colonnes numériques à l'aide de `StandardScaler`.

4. **Modélisation** :
   - **Régression Logistique** : Pour la classification binaire.
   - **Random Forest** : Pour la prédiction des prix.

5. **Optimisation** :
   - Utilisation de `GridSearchCV` pour ajuster les hyperparamètres des modèles.

6. **Évaluation** :
   - Mesures des performances via la précision (accuracy), le rapport de classification, et le R².

---

## **Résultats**

### **Régression Logistique**

- **Performances** (Classification binaire) :
  - **Accuracy** : `0.82`
  - **Rapport de classification** :

    ```bash
    Précision   Rappel  F1-score
    Classe 0    0.80    0.79    0.79
    Classe 1    0.82    0.83    0.82
    ```

### **Random Forest**

- **Performances** (Régression) :
  - **MSE** : `0.12`
  - **R²** : `0.87`
- **Meilleurs Paramètres** :
  - `n_estimators` : `100`
  - `max_depth` : `10`
  - `min_samples_split` : `2`
  - `min_samples_leaf` : `1`

---

## **Endpoints**

### **1. Read Root**

- **URL** : `/`
- **Méthode** : `GET`
- **Description** : Lit la racine.

### **2. Read Vehicules**

- **URL** : `/vehicules/`
- **Méthode** : `GET`
- **Description** : Lit les véhicules.

### **3. Create Vehicule**

- **URL** : `/vehicules/`
- **Méthode** : `POST`
- **Description** : Crée un nouveau véhicule.
- **Paramètres** :
  - `marque_id` : ID de la marque (integer)
  - `modele` : Modèle du véhicule (string)
  - `annee` : Année de fabrication (integer)
  - `kilometrage` : Kilométrage (integer)
  - `prix` : Prix (number)
  - `etat` : État du véhicule (string)
  - `carburant_id` : ID du carburant (integer)
  - `transmission_id` : ID de la transmission (integer)

### **4. Update Vehicule**

- **URL** : `/vehicules/{vehicule_id}`
- **Méthode** : `PUT`
- **Description** : Met à jour un véhicule existant.
- **Paramètres** :
  - `vehicule_id` : ID du véhicule (integer)
  - `marque_id` : ID de la marque (integer | null)
  - `modele` : Modèle du véhicule (string | null)
  - `annee` : Année de fabrication (integer | null)
  - `kilometrage` : Kilométrage (integer | null)
  - `prix` : Prix (number | null)
  - `etat` : État du véhicule (string | null)
  - `carburant_id` : ID du carburant (integer | null)
  - `transmission_id` : ID de la transmission (integer | null)

### **5. Delete Vehicule**

- **URL** : `/vehicules/{vehicule_id}`
- **Méthode** : `DELETE`
- **Description** : Supprime un véhicule existant.
- **Paramètres** :
  - `vehicule_id` : ID du véhicule (integer)

### **6. Predict**

- **URL** : `/predict`
- **Méthode** : `POST`
- **Description** : Prédit le prix d'un bien immobilier en fonction des caractéristiques fournies.
- **Paramètres** :
  - `features` : Caractéristiques du bien immobilier (JSON)
    - `kilometrage` : Kilométrage (number)
    - `annee` : Année de fabrication (integer)
    - `marque` : Marque du véhicule (string)
    - `carburant` : Type de carburant (string)
    - `transmission` : Type de transmission (string)
    - `modele` : Modèle du véhicule (string)
    - `etat` : État du véhicule (string)
- **Réponse** :
  - `200 OK` : Prédiction réussie avec le prix prédit
  - `400 Bad Request` : Paramètres manquants ou invalides

---

## **Conclusion**

Les modèles de régression logistique et de Random Forest ont montré des performances satisfaisantes pour leurs tâches respectives. La régression logistique a atteint une précision de 82% pour la classification binaire, tandis que le modèle Random Forest a obtenu un R² de 0.87 pour la prédiction des prix.

## **Installation**

Pour installer les dépendances nécessaires, exécutez la commande suivante :

```sh
pip install -r requirements.txt
```

## **Utilisation**

1. Clonez le dépôt :

    ```sh
    git clone https://github.com/Bastien-OC20/voitures_occasions.git
    ```

2. Accédez au répertoire du projet :

    ```sh
    cd voitures_occasions
    ```

### **Backend**

1. Lancez l'application FastAPI :

    ```sh
    uvicorn main:app --reload
    ```

### **Frontend**

1. Lancez l'application Streamlit :

    ```sh
    streamlit run app.py
    ```

### **Fonctionnalités de l'application Streamlit**

L'application Streamlit offre les fonctionnalités suivantes :

- **Connexion** : Permet aux utilisateurs de se connecter en utilisant leur nom d'utilisateur et leur mot de passe.
- **Inscription** : Permet aux nouveaux utilisateurs de s'inscrire en fournissant un nom d'utilisateur, une adresse e-mail et un mot de passe.
- **Page d'accueil** : Affiche un message de bienvenue aux utilisateurs connectés.
- **Prédiction des prix** : Permet aux utilisateurs de prédire le prix d'un véhicule en fonction de ses caractéristiques (kilométrage, année, marque, carburant, transmission, modèle, état).

## **Contributions**

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

## **Licence**

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

