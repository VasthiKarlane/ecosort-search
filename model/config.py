"""
Configuration centrale du projet EcoSort-Search.
Tous les hyperparamètres et chemins importants sont définis ici.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Chemins ---
# Chemins absolus (bases sur l'emplacement de ce fichier) afin que le modele
# se charge correctement quelle que soit le repertoire de travail (ex: dans Docker
# ou lorsque ce module est importe par l'application Flask dans app/).
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "raw")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "saved_model", "modele_eco_sort.h5")

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

# --- Mots-clés pour détecter les produits électroniques (D3E) ---
# Vérifiés AVANT d'utiliser le modèle IA, sur le nom du produit scrapé
D3E_KEYWORDS = [
    "chargeur", "charger", "smartphone", "telephone", "téléphone",
    "ecouteur", "écouteur", "casque", "batterie", "power bank",
    "montre connectee", "montre connectée", "mixeur", "blender",
    "cable usb", "câble usb", "adaptateur", "prise electrique",
    "ordinateur", "tablette", "console", "manette", "clavier",
    "souris", "enceinte", "bluetooth", "camera", "caméra"
]

# --- Couleurs UI associées à chaque catégorie officielle ---
CATEGORY_COLORS = {
    "JAUNE": "#F5B700",
    "VERT": "#16A34A",
    "BLEU": "#2563EB",
    "D3E": "#52525B",
    "MARRON": "#7C4A1E",
}

# --- Libellés et pictogrammes affichés dans l'interface ---
CATEGORY_LABELS = {
    "JAUNE": {"label": "Poubelle jaune", "icon": "🟡", "consigne": "Emballages recyclables : plastique, métal, carton"},
    "VERT": {"label": "Poubelle verte", "icon": "🟢", "consigne": "Verre d'emballage uniquement"},
    "BLEU": {"label": "Poubelle bleue", "icon": "🔵", "consigne": "Papiers et journaux"},
    "D3E": {"label": "Bac électronique (D3E)", "icon": "🔌", "consigne": "Appareils électriques et électroniques"},
    "MARRON": {"label": "Poubelle marron / noire", "icon": "⚫", "consigne": "Déchets résiduels non recyclables"},
}