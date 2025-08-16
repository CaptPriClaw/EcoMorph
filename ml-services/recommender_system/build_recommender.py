# ml-services/recommender_system/build_recommender.py

import os
import sys # --- NEW: Import sys
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# --- NEW: Code to add the project's root directory to the Python path ---
# This allows us to import from other folders like 'ai_registry'
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
# -----------------------------------------------------------------------

# --- CHANGED: The import is now absolute from the project root ---
from ml_services.ai_registry.base_pipeline import preprocess_text


def build_model():
    """
    Builds the TF-IDF vectorizer and product matrix from a dataset
    and saves them to .pkl files.
    """
    print("Building recommender model...")

    # --- 1. The Dataset ---
    product_data = {
        'name': [
            "T-Shirt Tote Bag", "Glass Jar Lantern", "Denim Jean Patches",
            "Wine Bottle Bird Feeder", "Plastic Bottle Planter", "Newspaper Seedling Pots",
            "Tin Can Utensil Holder", "CD Mosaic Mirror", "Magazine Page Coasters",
            "Sock Puppet", "Tire Swing", "Old Book Safe"
        ],
        'description': [
            "A reusable shopping bag made from an old cotton t-shirt.",
            "A decorative lantern crafted from a glass jar, wire, and a tea light.",
            "Customizable patches for clothing made from scrap denim jean material.",
            "A simple bird feeder constructed from an inverted wine bottle.",
            "A self-watering vertical planter made from plastic soda bottles.",
            "Biodegradable pots for starting seeds, made from rolled newspaper.",
            "A colorful kitchen utensil holder created from a painted tin can.",
            "A decorative mirror frame adorned with mosaic pieces from broken CDs.",
            "Durable drink coasters made from rolled and sealed magazine pages.",
            "A classic children's toy made from a single, mismatched sock.",
            "An outdoor swing for kids made from a recycled vehicle tire.",
            "A hidden storage box created by hollowing out a thick, old book."
        ]
    }
    df = pd.DataFrame(product_data)

    # --- 2. Preprocess the Text ---
    print("Preprocessing product descriptions...")
    df['clean_description'] = df['description'].apply(preprocess_text)

    # --- 3. Train the TF-IDF Vectorizer ---
    print("Training TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['clean_description'])

    # --- 4. Save the Files ---
    # Save the trained vectorizer object
    vectorizer_path = os.path.join(current_dir, 'vectorizer.pkl')
    joblib.dump(vectorizer, vectorizer_path)
    print(f"Vectorizer saved to: {vectorizer_path}")

    # Save the TF-IDF matrix and the product names for lookup
    model_data = {
        'matrix': tfidf_matrix,
        'names': df['name'].tolist()
    }
    model_path = os.path.join(current_dir, 'model.pkl')
    joblib.dump(model_data, model_path)
    print(f"Model data saved to: {model_path}")

    print("\nBuild complete. Your .pkl files are ready!")


if __name__ == "__main__":
    build_model()