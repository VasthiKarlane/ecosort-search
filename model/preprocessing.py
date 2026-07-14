from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Paramètres
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
DATA_PATH = "../data/raw"  # chemin relatif depuis model/

def get_data_generators():
    """
    Prépare les générateurs d'images pour l'entraînement et la validation.
    Redimensionne, normalise et sépare automatiquement les données.
    """
    datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=0.3
    )

    train_generator = datagen.flow_from_directory(
        DATA_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training"
    )

    validation_generator = datagen.flow_from_directory(
        DATA_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation"
    )

    return train_generator, validation_generator


if __name__ == "__main__":
    train_gen, val_gen = get_data_generators()
    print("Classes détectées :", train_gen.class_indices)
    print("Nombre d'images d'entraînement :", train_gen.samples)
    print("Nombre d'images de validation :", val_gen.samples)