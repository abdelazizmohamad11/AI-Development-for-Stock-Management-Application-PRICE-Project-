from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import joblib
import os


def train_models(df):
    # Dictionary to store models for each EAN
    models = {}
    rmse_values = {}  # Dictionary to store RMSE per EAN

    # Train a model for each EAN
    for ean in df["EAN"].unique():
        ean_data = df[df["EAN"] == ean]  # Filter data for specific EAN

        # Create lagged features
        ean_data["Lag_1"] = ean_data["Total_Weekly_Consumption"].shift(1)
        ean_data["Lag_2"] = ean_data["Total_Weekly_Consumption"].shift(2)
        ean_data["Lag_3"] = ean_data["Total_Weekly_Consumption"].shift(3)
        ean_data["Lag_4"] = ean_data["Total_Weekly_Consumption"].shift(4)

        ean_data = ean_data.dropna()  # Drop rows with NaN values

        # Split into features (X) and target (y)
        X = ean_data[["Lag_1", "Lag_2", "Lag_3", "Lag_4"]]  # Use lagged values as features
        y = ean_data["Total_Weekly_Consumption"]

        # Train-test split (keep last 20% for testing)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        # Train Random Forest model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Store model
        models[ean] = model

        # Predict and evaluate
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Store RMSE for this EAN
        rmse_values[ean] = rmse

        print(f"EAN {ean} - RMSE: {rmse:.4f}")

    return models, rmse_values


if __name__ == "__main__":
    # Load the preprocessed data
    df = pd.read_csv("../Dataset/weekly_consumption.csv")

    # Train models
    models, rmse_values = train_models(df)

    # Clean the models directory
    models_dir = "../Models/randomforest_models"
    for filename in os.listdir(models_dir):
        file_path = os.path.join(models_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    # Save the models and metrics
    joblib.dump(models, os.path.join(models_dir, "random_forest_models_improved.pkl"))
    joblib.dump(rmse_values, os.path.join(models_dir, "random_forest_rmse_values_improved.pkl"))
