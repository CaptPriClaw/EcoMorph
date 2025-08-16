# ml-services/credit_predictor/evaluate.py

import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import os

def evaluate_model():
    """
    Loads the trained model and a test dataset, evaluates the model's
    performance, and prints the key metrics.
    """
    # Define paths relative to this script's location
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'model.pkl')
    test_data_path = os.path.join(current_dir, 'data/test_credit_data.csv') # Assumes test data is in a subfolder

    # --- 1. Load Model and Data ---
    print("Loading trained model and test data...")
    try:
        model = joblib.load(model_path)
        test_df = pd.read_csv(test_data_path)
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure 'model.pkl' and 'data/test_credit_data.csv' exist.")
        return

    # --- 2. Prepare Data ---
    # Assume the last column is the target variable ('exchange_rate')
    X_test = test_df.iloc[:, :-1]
    y_test = test_df.iloc[:, -1]

    print(f"Evaluating model on {len(test_df)} test samples...")

    # --- 3. Make Predictions ---
    predictions = model.predict(X_test)

    # --- 4. Calculate Metrics ---
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    # --- 5. Print Results ---
    print("\n--- Model Evaluation Results ---")
    print(f"  Mean Absolute Error (MAE):    {mae:.4f}")
    print(f"  Mean Squared Error (MSE):     {mse:.4f}")
    print(f"  Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"  R-squared (R²):               {r2:.4f}")
    print("---------------------------------")
    print("\nEvaluation complete.")


if __name__ == "__main__":
    evaluate_model()