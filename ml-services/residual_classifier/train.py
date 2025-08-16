# ml-services/residual_classifier/train.py

import os
import numpy as np
import joblib
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Define image dimensions for preprocessing
IMAGE_SIZE = (64, 64)


def image_to_feature_vector(image_path):
    """Loads an image, resizes it, converts to grayscale, and flattens it."""
    try:
        with Image.open(image_path) as img:
            # Resize and convert to grayscale
            processed_img = img.resize(IMAGE_SIZE).convert('L')
            # Flatten the 2D image array into a 1D vector
            return np.array(processed_img).flatten()
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None


def load_dataset(dataset_path):
    """Loads image data and labels from a structured folder."""
    features = []
    labels = []

    for label, category in enumerate(['residual', 'usable']):
        folder_path = os.path.join(dataset_path, category)
        if not os.path.isdir(folder_path):
            continue

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                feature_vector = image_to_feature_vector(image_path)

                if feature_vector is not None:
                    features.append(feature_vector)
                    labels.append(label)  # 0 for residual, 1 for usable

    return np.array(features), np.array(labels)


def train_classifier():
    """Main function to train the classifier and save the model."""
    current_dir = os.path.dirname(__file__)
    train_data_path = os.path.join(current_dir, 'data/train')
    model_path = os.path.join(current_dir, 'model.pkl')

    # --- 1. Load the dataset ---
    print("Loading dataset...")
    X, y = load_dataset(train_data_path)

    if len(X) == 0:
        print("Dataset not found or is empty. Please check the data folder structure.")
        return

    # --- 2. Split data for validation ---
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training on {len(X_train)} images, validating on {len(X_val)} images.")

    # --- 3. Initialize and Train the Model ---
    print("Training RandomForestClassifier...")
    # A simple RandomForest is a good starting point for this task.
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # --- 4. Validate the Model ---
    y_pred = model.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred)
    print(f"Validation Accuracy: {accuracy:.2%}")

    # --- 5. Save the Trained Model ---
    joblib.dump(model, model_path)
    print(f"\nModel trained and saved to: {model_path}")


if __name__ == "__main__":
    train_classifier()