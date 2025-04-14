# PRICE Prediction Project - LET'STOCK

This project focuses on predicting product prices using historical data and advanced machine learning techniques, followed by the development of a user-friendly graphical interface for deployment. It was conducted as part of a collaboration with LET'STOCK, a client seeking to automate and enhance pricing predictions.

## Project Overview
- Created by: Abdelaziz Mohamad
- Project Type: End-to-End Machine Learning Pipeline + GUI Application
- Technologies: Python, Scikit-learn, Keras, Tkinter, Pandas, Matplotlib

## Full ML Pipeline Implementation

### 1. Data Analysis & Exploration
- Conducted thorough analysis to understand the distribution, correlation, and patterns in the dataset.
- Detected and handled missing values, outliers, and irregularities.
- Visualized important features and price trends to inform feature engineering.

### 2. Data Preprocessing
- Normalization and encoding of categorical features.
- Removed low-quality and irrelevant columns.
- Split the dataset into training and testing sets using an 80-20 split.

### 3. Model Training & Evaluation
We trained three models to perform regression on the cleaned dataset:

- **Random Forest Regressor**
- **K-Nearest Neighbors Regressor**
- **Recurrent Neural Network (RNN)** using TensorFlow/Keras

The models were evaluated based on **RMSE (Root Mean Squared Error)**:

- Random Forest: Lowest RMSE, most robust and generalizable results.
- KNN: Reasonable performance, but less accurate than RF.
- RNN: Captured temporal dependencies but required extensive tuning and performed below Random Forest.

> **Conclusion:** The **Random Forest** model was selected as the final model due to its superior performance in terms of RMSE and reliability.

### 4. User Interface Development
A desktop application was built using **Tkinter** to allow non-technical users to:
- Load new data for prediction.
- Trigger the prediction pipeline with a single click.
- Visualize predicted vs. actual prices using Matplotlib.
- Export predictions to a **CSV** file.

## Features
- **Full ML Pipeline:** From raw data preprocessing to model training, selection, and evaluation.
- **Model Comparison:** Evaluated and compared performance of RF, KNN, and RNN.
- **Best Model Selection:** RF model retained for production use based on RMSE results.
- **Desktop Interface:** Built with Tkinter for easy interaction and visualization.
- **Prediction Export:** Ability to export predictions into a .CSV file for integration with client systems.

## How to Start the App

This step is under development. The goal is to create a packaged **executable file (.exe)** so the user can run the app directly without launching Python.

### To Run Locally:
1. Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```
2. Launch the interface:
```bash
python app.py
```

## Future Improvements
- Develop an executable version of the application to simplify usage.
- Automatically check and install missing dependencies on execution.
- Add multi-language support.
- Include real-time data updating from client databases.
- Optimize the RNN for more temporal-based features.

## Important Note
This repository **does not include the dataset** due to usage consent and privacy agreements with the client **LET'STOCK**.

> The project is uploaded solely for **demonstration purposes**. Only LET'STOCK has authorization to use the full system with the dataset.

## Ongoing Work
This project is **still ongoing**. The following are planned for the next version:
- Packaging the app into a single executable file (.exe)
- CSV export of predictions for client integration
- Dependency auto-check and installation before launch

---

Thank you for checking out this project!
