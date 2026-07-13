from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

import config
from preprocessing import get_data_generators


def build_model(num_classes):
    """
    Construit le modèle par Transfer Learning à partir de MobileNetV2.
    """
    base_model = MobileNetV2(
        input_shape=(*config.IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(
        optimizer=Adam(learning_rate=config.LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def get_class_weights(train_generator):
    """
    Calcule des poids par catégorie pour compenser le déséquilibre du dataset
    (ex: 'trash' qui a moins d'images que les autres).
    """
    classes = train_generator.classes
    class_labels = np.unique(classes)

    weights = compute_class_weight(
        class_weight="balanced",
        classes=class_labels,
        y=classes
    )

    return dict(zip(class_labels, weights))


if __name__ == "__main__":
    # 1. Charger les données
    train_generator, validation_generator = get_data_generators()

    # 2. Construire le modèle
    model = build_model(num_classes=len(config.DATASET_CLASSES))
    model.summary()

    # 3. Calculer les poids de classes (pour compenser le déséquilibre)
    class_weights = get_class_weights(train_generator)
    print("\nPoids par catégorie :", class_weights)

    # 4. Définir l'arrêt anticipé (EarlyStopping)
    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True
    )

    # 5. Entraîner le modèle
    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=config.EPOCHS,
        class_weight=class_weights,
        callbacks=[early_stop]
    )

    # 6. Sauvegarder le modèle entraîné
    model.save(config.MODEL_SAVE_PATH)
    print(f"\nModèle sauvegardé dans : {config.MODEL_SAVE_PATH}")