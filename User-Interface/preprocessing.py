import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib


def preprocess_data(filename):
    dataset_folder = "../Dataset"
    input_path = os.path.join(dataset_folder, filename)

    # Load dataset
    df = pd.read_csv(input_path)

    ### Convert Date Column to Datetime Format and Extract Week-Based Features
    # Remove the time part (anything after the year)
    df["Creation Date"] = df["Creation Date"].str.extract(r"([A-Za-z]+ \d{1,2}, \d{4})")

    # Convert to datetime with the correct format
    df["Creation Date"] = pd.to_datetime(df["Creation Date"], format="%b %d, %Y")

    # Since we predict on a per-week basis, we extract week-related features

    # Get the year-week format (e.g., "2024-03" for the 3rd week of 2024)
    df["Creation_Week"] = df["Creation Date"].dt.strftime('%Y-%U')

    # Extract the week number separately (useful for tracking seasonal patterns)
    df["Week_Number"] = df["Creation Date"].dt.isocalendar().week

    # Extract the year for further grouping if needed
    df["Year"] = df["Creation Date"].dt.year

    ### Aggregate Weekly Consumption Per Product
    # Group by EAN and week, summing up the Quantite
    weekly_consumption = df.groupby(["EAN", "Creation_Week"])["Quantite"].sum().reset_index()

    # Rename columns for clarity
    weekly_consumption.rename(columns={"Quantite": "Total_Weekly_Consumption"}, inplace=True)

    ### Handle Missing Weeks
    # Some products might not be sold every week, leading to missing data
    # To ensure a continuous time series, we fill missing weeks with 0

    # Get all unique weeks in the dataset
    all_weeks = df["Creation_Week"].unique()

    # Get all unique products (EANs)
    products = df["EAN"].unique()

    # Create a full index of all possible (EAN, Week) combinations
    complete_index = pd.MultiIndex.from_product([products, all_weeks], names=["EAN", "Creation_Week"])

    # Reindex the DataFrame to fill in missing weeks with 0
    weekly_consumption = weekly_consumption.set_index(["EAN", "Creation_Week"]).reindex(complete_index,
                                                                                        fill_value=0).reset_index()

    ### 1. Remove records where EAN is null
    weekly_consumption = weekly_consumption.dropna(subset=["EAN"])

    ### 3. Convert Creation_Week to a Proper Datetime Object
    weekly_consumption['Week_Start'] = weekly_consumption['Creation_Week'].apply(
        lambda x: pd.to_datetime(x + '-1', format='%Y-%U-%w')
    )

    ### 4. Encode EAN as a Categorical Variable
    weekly_consumption['EAN'] = weekly_consumption['EAN'].astype(str)

    ### 5. Normalize Numerical Features
    scaler = StandardScaler()
    weekly_consumption[['Total_Weekly_Consumption']] = scaler.fit_transform(
        weekly_consumption[['Total_Weekly_Consumption']]
    )

    # Save the scaler
    joblib.dump(scaler, "../scaler.pkl")

    ### 6. Sort the Data by Product and Week
    weekly_consumption.sort_values(["EAN", "Week_Start"], inplace=True)

    ### Export the cleaned data to CSV
    weekly_consumption.to_csv("../Dataset/weekly_consumption.csv", index=False)
    print(f"Preprocessing complete! Saved as weekly_consumption in Dataset folder")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No filename provided!")
        sys.exit(1)

    filename = sys.argv[1]
    preprocess_data(filename)
