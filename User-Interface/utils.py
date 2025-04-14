import pandas as pd
import joblib
import os


def load_models():
    """Loads the pre-trained models and scaler."""
    models_path = "../Models/randomforest_models/random_forest_models_improved.pkl"
    scaler_path = "../scaler.pkl"

    if not os.path.exists(models_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError("Model or scaler file is missing!")

    models = joblib.load(models_path)
    scaler = joblib.load(scaler_path)

    return models, scaler


def load_dataset():
    """Loads the preprocessed dataset."""
    dataset_path = "../Dataset/weekly_consumption.csv"

    if not os.path.exists(dataset_path):
        raise FileNotFoundError("Dataset not found! Please upload and preprocess a dataset.")

    return pd.read_csv(dataset_path)
