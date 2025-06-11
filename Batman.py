# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 23:35:38 2025

@author: Hemal
"""
    

import streamlit as st
import pandas as pd

st.title('Option Chain Analysis')

# File upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file
    data = pd.read_csv(uploaded_file)

    # Ensure the "High" column is numeric
    data['High  '] = pd.to_numeric(data['High  '], errors='coerce')

    # Fill missing values in the "High" column
    data['High  '].fillna(0, inplace=True)

    # Extract unique strike prices and sort them
    strike_prices = sorted(data['Strike Price  '].unique())

    # Current underlying value
    underlying_value = data["Underlying Value  "].iloc[0]

    # Find the ATM strike price
    atm_strike = min(strike_prices, key=lambda x: abs(x - underlying_value))

    # Find the index of the ATM strike
    atm_index = strike_prices.index(atm_strike)

    # List ATM strike and 10 strikes above and below
    selected_strikes = strike_prices[atm_index - 10 : atm_index + 11]

    # Calculate absolute distance from ATM strike price
    distances = [abs(strike - atm_strike) for strike in selected_strikes]

    # Provide weights in inverse proportion to distance
    weights = [1 / (distance + 1) for distance in distances]  # Adding 1 to avoid division by zero

    # Multiply weight with the HIGH column
    weighted_highs = []
    for strike in selected_strikes:
        high_values = data.loc[data['Strike Price  '] == strike, 'High  ']
        high_value = high_values.values[0]
        weight = weights[selected_strikes.index(strike)]
        weighted_highs.append(high_value * weight)

    # Sum up the weighted high values
    sum_weighted_highs = sum(weighted_highs)

    st.write("ATM Strike Price:", atm_strike)
    st.write("Selected Strikes:", selected_strikes)
    st.write("Distances from ATM Strike:", distances)
    st.write("Weights:", weights)
    st.write("Weighted Highs:", weighted_highs)
    st.write("Sum of Weighted Highs:", sum_weighted_highs)
