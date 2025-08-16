# ml-services/residual_classifier/inference.py

import os
import io
import joblib
import numpy as np
from PIL import Image

# Use the same image size as defined in the training script
IMAGE_SIZE = (64, 64)
CLASS_MAP = {0: 'residual', 1: 'usable'}  # Map numeric labels to names


class ResidualClassifier:
    """
    A class to load the trained classifier and run inference on new images.
    """

    def __init__(self):
        """
        Loads the pre-trained model from the .pkl file.
        """
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, 'model.pkl')

        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            print(f"Error: Model file not found at {model_path}")
            print("Please run the train.py script first to generate the model.")
            self.model = None

    def _preprocess_image(self, image_bytes):
        """
        Takes image bytes, preprocesses the image to match the training
        format, and returns a feature vector.
        """
        # Open the image from in-memory bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Resize, convert to grayscale, and flatten
        processed_img = image.resize(IMAGE_SIZE).convert('L')
        feature_vector = np.array(processed_img).flatten()

        # Reshape for a single prediction
        return feature_vector.reshape(1, -1)

    def run_inference(self, image_bytes) -> dict:
        """
        Runs inference on a single image.

        Args:
            image_bytes: The raw bytes of the image file.

        Returns:
            A dictionary containing the predicted class and confidence score.
        """
        if self.model is None:
            return {"error": "Classifier model is not loaded."}

        # 1. Preprocess the image to create a feature vector
        feature_vector = self._preprocess_image(image_bytes)

        # 2. Predict the class (0 or 1)
        prediction = self.model.predict(feature_vector)
        predicted_class_index = prediction[0]

        # 3. Get the prediction probabilities (confidence scores)
        probabilities = self.model.predict_proba(feature_vector)
        confidence = probabilities[0][predicted_class_index]

        # 4. Map the numeric label back to its name
        predicted_class_name = CLASS_MAP[predicted_class_index]

        return {
            "predicted_class": predicted_class_name,
            "confidence": float(confidence)
        }


# Example usage:
if __name__ == '__main__':
    # This block will only run if you have created the model.pkl file.
    classifier = ResidualClassifier()

    if classifier.model:
        # Create a dummy black image for testing purposes
        dummy_image = Image.new('L', IMAGE_SIZE, color='black')

        # Save the image to an in-memory byte stream
        byte_stream = io.BytesIO()
        dummy_image.save(byte_stream, format='PNG')
        image_bytes = byte_stream.getvalue()

        # Run inference
        result = classifier.run_inference(image_bytes)
        print(f"Inference Result for dummy image: {result}")