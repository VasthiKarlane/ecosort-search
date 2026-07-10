"""
Configuration centrale du projet EcoSort-Search.
Tous les hyperparamètres et chemins importants sont définis ici.
"""

# --- Chemins ---
DATA_PATH = "../data/raw"
MODEL_SAVE_PATH = "saved_model/modele_eco_sort.h5"

# --- Prétraitement des images ---
IMG_SIZE = (224, 224)      # Taille standard pour MobileNetV2
BATCH_SIZE = 32            # Nombre d'images traitées en même temps
VALIDATION_SPLIT = 0.3     # 30% des données réservées à la validation

# --- Entraînement ---
EPOCHS = 20                # Nombre de fois où le modèle voit tout le dataset
LEARNING_RATE = 0.0001     # Vitesse d'apprentissage du modèle

# --- Catégories du dataset (issues de Kaggle) ---
DATASET_CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

# --- Mapping vers les catégories officielles du sujet (Tâche A.9, à venir) ---
CATEGORY_MAPPING = {
    "plastic": "JAUNE",
    "metal": "JAUNE",
    "cardboard": "JAUNE",
    "glass": "VERT",
    "paper": "BLEU",
    "trash": "MARRON",
}