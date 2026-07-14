import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import config


def get_eval_generator():
    """
    Générateur dédié à l'évaluation, avec shuffle=False
    pour garantir que l'ordre des prédictions correspond à l'ordre des vraies étiquettes.
    """
    datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=config.VALIDATION_SPLIT
    )

    eval_generator = datagen.flow_from_directory(
        config.DATA_PATH,
        target_size=config.IMG_SIZE,
        batch_size=config.BATCH_SIZE,
        class_mode="categorical",
        subset="validation",
        shuffle=False  # <-- LA CORRECTION CLÉ
    )

    return eval_generator


def evaluate_model():
    # 1. Charger le modèle entraîné
    model = load_model(config.MODEL_SAVE_PATH)

    # 2. Générateur d'évaluation SANS mélange
    eval_generator = get_eval_generator()

    # 3. Prédire sur toutes les images de validation, dans l'ordre
    predictions = model.predict(eval_generator, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)

    # 4. Récupérer les vraies étiquettes (maintenant dans le même ordre)
    true_classes = eval_generator.classes
    class_labels = list(eval_generator.class_indices.keys())

    # 5. Rapport de classification détaillé
    print("\n--- Rapport de classification ---")
    print(classification_report(true_classes, predicted_classes, target_names=class_labels))

    # 6. Matrice de confusion
    cm = confusion_matrix(true_classes, predicted_classes)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_labels)

    fig, ax = plt.subplots(figsize=(8, 8))
    disp.plot(ax=ax, cmap="Blues", xticks_rotation=45)
    plt.title("Matrice de confusion - EcoSort")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")
    print("\nMatrice de confusion sauvegardée dans model/confusion_matrix.png")
    plt.show()


if __name__ == "__main__":
    evaluate_model()