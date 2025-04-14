import numpy as np
import pandas as pd


def predict_consumption(ean, df, models, scaler):
    if ean in models:
        # Filter data for the specific EAN
        ean_data = df[df["EAN"] == ean].copy()

        # Ensure 'Week_Start' is in datetime format
        ean_data["Week_Start"] = pd.to_datetime(ean_data["Week_Start"])

        # Inverse transform past consumption values (if they are scaled)
        past_consumption_scaled = ean_data["Total_Weekly_Consumption"].values.reshape(-1, 1)
        ean_data["Total_Weekly_Consumption"] = scaler.inverse_transform(past_consumption_scaled).flatten()

        # Create lagged features
        ean_data["Lag_1"] = ean_data["Total_Weekly_Consumption"].shift(1)
        ean_data["Lag_2"] = ean_data["Total_Weekly_Consumption"].shift(2)
        ean_data["Lag_3"] = ean_data["Total_Weekly_Consumption"].shift(1)
        ean_data["Lag_4"] = ean_data["Total_Weekly_Consumption"].shift(2)
        ean_data = ean_data.dropna()  # Drop rows with NaN values

        # Get the last known values for Lag_1 and Lag_2
        last_lag_1 = ean_data["Lag_1"].iloc[-1]
        last_lag_2 = ean_data["Lag_2"].iloc[-1]
        last_lag_3 = ean_data["Lag_3"].iloc[-1]
        last_lag_4 = ean_data["Lag_4"].iloc[-1]
        last_week_start = ean_data["Week_Start"].iloc[-1]  # Get last recorded date

        # Create future features for the next 4 weeks
        future_predictions_scaled = []
        future_dates = []  # To store the corresponding future weeks

        for i in range(1, 5):
            # Predict the next week's consumption (scaled)
            future_features = np.array([[last_lag_1, last_lag_2, last_lag_3, last_lag_4]])
            future_prediction_scaled = models[ean].predict(future_features)[0]
            future_predictions_scaled.append(future_prediction_scaled)

            # Compute next week's start date
            next_week_start = last_week_start + pd.Timedelta(weeks=i)
            future_dates.append(next_week_start)

            # Update lagged values for the next prediction
            last_lag_4 = last_lag_3
            last_lag_3 = last_lag_3
            last_lag_2 = last_lag_1
            last_lag_1 = future_prediction_scaled

        # Inverse transform the predictions to get actual values
        future_predictions = scaler.inverse_transform(
            np.array(future_predictions_scaled).reshape(-1, 1)
        ).flatten()

        # Convert to integer values
        future_predictions = np.round(future_predictions).astype(int)

        return future_dates, future_predictions, ean_data
    else:
        return None, None, None
