import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Charger les données
df = pd.read_csv('data/cleaned/voitures_aramisauto_nettoye.csv')

# Encodage One-Hot des colonnes catégorielles
categorical_cols = df.select_dtypes(include=['object']).columns
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Ajouter la variable binaire 'Prix_binaire'
threshold = df['Prix'].median()
df_encoded['Prix_binaire'] = (df['Prix'] > threshold).astype(int)

# Standardiser les données numériques
scaler = StandardScaler()
numeric_cols = df_encoded.select_dtypes(include=['int64', 'float64']).columns
df_encoded[numeric_cols] = scaler.fit_transform(df_encoded[numeric_cols])

# **Modèle de Régression Non Linéaire - Random Forest**
# Préparation des données pour la régression
X_regression = df_encoded.drop(columns=['Prix', 'Prix_binaire'])
y_regression = df_encoded['Prix']

# Division des données en ensemble d'entraînement et de test
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_regression, y_regression, test_size=0.2, random_state=42)

# Définir la grille d'hyperparamètres pour Random Forest
param_grid = {
    'n_estimators': [50, 100],      # Nombre d'arbres
    'max_depth': [None, 10, 20],    # Profondeur maximale des arbres
    'min_samples_split': [2, 5],    # Nombre minimum d'échantillons pour diviser un nœud
    'min_samples_leaf': [1, 2, 4],      # Nombre minimum d'échantillons dans une feuille
    'max_features': ['sqrt'],   # Nombre de caractéristiques à considérer pour la division
    'bootstrap': [True, False]         
}

# Configurer GridSearchCV
grid_search = GridSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_grid=param_grid,
    cv=3,                              # Validation croisée à 5 plis
    scoring='r2',                      # Optimiser le R²
    verbose=2,                         # Afficher des informations pendant la recherche
    n_jobs=-1                          # Utiliser tous les cœurs disponibles
)

# Lancer la recherche
grid_search.fit(X_train_reg, y_train_reg)

# Afficher les meilleurs paramètres et le meilleur score R²
print("\nMeilleurs hyperparamètres :")
print(f"Meilleur R² pendant la validation croisée : {grid_search.best_score_:.2f}")

# Utiliser le meilleur modèle trouvé
best_forest_model = grid_search.best_estimator_

# Faire des prédictions
y_pred_best_forest = best_forest_model.predict(X_test_reg)

# Évaluer les performances
mse_best_forest = mean_squared_error(y_test_reg, y_pred_best_forest)
r2_best_forest = r2_score(y_test_reg, y_pred_best_forest)

print("\nÉvaluation du modèle optimisé :")
print(f"MSE : {mse_best_forest:.2f}")
print(f"R² : {r2_best_forest:.2f}")