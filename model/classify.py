"""
Fonction finale de classification EcoSort.
Combine détection D3E par mots-clés + prédiction du modèle IA.
"""
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

import config

# Charger le modèle une seule fois (pas à chaque appel)
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = load_model(config.MODEL_SAVE_PATH)
    return _model


def is_d3e(product_name):
    """
    Vérifie si le nom du produit correspond à un équipement électronique (D3E),
    en cherchant des mots-clés connus.
    """
    product_name_lower = product_name.lower()
    return any(keyword in product_name_lower for keyword in config.D3E_KEYWORDS)


def predict_category(image_path, product_name=""):
    """
    Détermine la catégorie de tri officielle d'un produit.

    1. Vérifie d'abord si le nom du produit indique un déchet électronique (D3E)
    2. Sinon, utilise le modèle IA sur l'image pour prédire la matière,
       puis applique le mapping vers la catégorie officielle.
    """
    # Étape 1 : détection D3E par mots-clés
    if product_name and is_d3e(product_name):
        return {
            "category": "D3E",
            "color": config.CATEGORY_COLORS["D3E"],
            "detected_material": None,
            "method": "keyword"
        }

    # Étape 2 : prédiction par le modèle IA
    model = _get_model()

    img = keras_image.load_img(image_path, target_size=config.IMG_SIZE)
    img_array = keras_image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)
    predicted_index = np.argmax(predictions[0])
    detected_material = config.DATASET_CLASSES[predicted_index]
    confidence = float(predictions[0][predicted_index])

    official_category = config.CATEGORY_MAPPING[detected_material]

    return {
        "category": official_category,
        "color": config.CATEGORY_COLORS[official_category],
        "detected_material": detected_material,
        "confidence": round(confidence, 3),
        "method": "model"
    }


if __name__ == "__main__":
    # Petit test avec une image d'exemple du dataset
    import os
    test_folder = os.path.join(config.DATA_PATH, "glass")
    test_image = os.path.join(test_folder, os.listdir(test_folder)[0])

    result = predict_category(test_image, product_name="Bouteille en verre")
    print("Résultat du test :", result)

    result_d3e = predict_category(test_image, product_name="Chargeur de téléphone rapide")
    print("Résultat du test D3E :", result_d3e)