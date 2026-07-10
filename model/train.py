from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

import config


def build_model(num_classes):
    """
    Construit le modèle par Transfer Learning à partir de MobileNetV2.
    """
    # 1. Charger MobileNetV2 pré-entraîné, sans sa couche de classification finale
    base_model = MobileNetV2(
        input_shape=(*config.IMG_SIZE, 3),  # (224, 224, 3) -> 3 = couleurs RGB
        include_top=False,                   # on enlève la dernière couche
        weights="imagenet"                   # on charge les poids pré-entraînés
    )

    # 2. Geler les couches de MobileNetV2 (on ne les entraîne pas)
    base_model.trainable = False

    # 3. Ajouter nos propres couches finales, adaptées à nos 6 catégories
    x = base_model.output
    x = GlobalAveragePooling2D()(x)   # résume chaque "carte de caractéristiques" en un seul nombre
    x = Dense(128, activation="relu")(x)  # couche intermédiaire
    x = Dropout(0.3)(x)                    # évite le sur-apprentissage (voir explication plus bas)
    predictions = Dense(num_classes, activation="softmax")(x)  # couche finale : nos 6 catégories

    # 4. Assembler le modèle complet
    model = Model(inputs=base_model.input, outputs=predictions)

    # 5. Compiler le modèle (préparer l'entraînement)
    model.compile(
        optimizer=Adam(learning_rate=config.LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":
    model = build_model(num_classes=len(config.DATASET_CLASSES))
    model.summary()