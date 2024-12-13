import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

# Function to load and train the model
def train_model():
    # Load the dataset
    data = pd.read_csv('cleaned_dataset (1).csv')  # Ensure this file is in the same directory
    
    # Define features and target
    features = ['Rainfall_mm', 'Fertilizer_Used', 'Irrigation_Used', 'Temperature_Celsius', 'Days_to_Harvest']
    target = 'Yield_tons_per_hectare'

    X = data[features]
    y = data[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Train the XGBoost model
    xgb_model = XGBRegressor(random_state=42)
    xgb_model.fit(X_train_scaled, y_train)

    return xgb_model, scaler

# Load and train the model
xgb_model, scaler = train_model()

# Streamlit UI
st.title("Crop Yield Prediction App 🌾")
st.write("Enter the feature values below to predict the yield (tons per hectare).")

# Input fields for features
rainfall = st.number_input("Rainfall (mm):", min_value=0.0, max_value=500.0, step=1.0, value=100.0)
fertilizer_used = st.number_input("Fertilizer Used (kg):", min_value=0.0, max_value=300.0, step=1.0, value=100.0)
irrigation_used = st.selectbox("Irrigation Used (Yes=1, No=0):", [0, 1])
temperature = st.number_input("Temperature (°C):", min_value=0.0, max_value=50.0, step=0.1, value=25.0)
days_to_harvest = st.number_input("Days to Harvest:", min_value=0, max_value=200, step=1, value=90)

# Predict button
if st.button("Predict Yield"):
    # Prepare the input array
    input_features = np.array([[rainfall, fertilizer_used, irrigation_used, temperature, days_to_harvest]])
    input_features_scaled = scaler.transform(input_features)  # Scale the input
    
    # Make the prediction
    predicted_yield = xgb_model.predict(input_features_scaled)[0]

    # Display the prediction
    st.success(f"The predicted yield is: **{predicted_yield:.2f} tons per hectare**") 
