# ml-services/credit_predictor/train_model.py

import pandas as pd
import xgboost as xgb
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression


def create_synthetic_data(num_samples=1000):
    """Creates a synthetic dataset for training the credit predictor model."""
    print(f"Generating {num_samples} synthetic data samples...")
    # These features represent market conditions that might affect point values
    features, target = make_regression(
        n_samples=num_samples,
        n_features=4,
        n_informative=3,
        noise=20,
        random_state=42
    )

    feature_names = ['material_demand', 'waste_supply', 'market_saturation', 'seasonal_factor']
    df = pd.DataFrame(features, columns=feature_names)
    df['exchange_rate'] = target  # This is what we want to predict

    # Make the data more realistic
    df['material_demand'] = abs(df['material_demand'])
    df['exchange_rate'] = abs(df['exchange_rate']) + 50  # Ensure positive rates

    # Create a directory for the data if it doesn't exist
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Split data into training and testing sets and save them
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df.to_csv(os.path.join(data_dir, 'train_credit_data.csv'), index=False)
    test_df.to_csv(os.path.join(data_dir, 'test_credit_data.csv'), index=False)

    print("Synthetic data created and saved.")
    return train_df


def train_model():
    """
    Loads training data, trains an XGBoost model, and saves it to a .pkl file.
    """
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'model.pkl')
    train_data_path = os.path.join(current_dir, 'data/train_credit_data.csv')

    # --- 1. Load or Create Data ---
    try:
        train_df = pd.read_csv(train_data_path)
        print("Loaded existing training data.")
    except FileNotFoundError:
        print("Training data not found. Generating new synthetic data...")
        train_df = create_synthetic_data()

    # --- 2. Prepare Data for Training ---
    X_train = train_df.drop('exchange_rate', axis=1)
    y_train = train_df['exchange_rate']

    # --- 3. Initialize and Train the Model ---
    print("Training XGBoost Regressor model...")
    # These hyperparameters can be tuned for better performance
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    model.fit(X_train, y_train)
    print("Model training complete.")

    # --- 4. Save the Trained Model ---
    joblib.dump(model, model_path)
    print(f"Model successfully saved to: {model_path}")


if __name__ == "__main__":
    train_model()