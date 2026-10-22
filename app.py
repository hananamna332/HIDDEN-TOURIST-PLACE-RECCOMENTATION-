
import streamlit as st
import pandas as pd

st.title("AI Hidden Tourist Spot Recommender")

# Read tourist data
data = pd.read_csv("attractions.csv")

# Get user preferences
location = st.selectbox("Choose location", data["location"].unique())

interest = st.selectbox("Choose your interest", data["category"].unique())

budget = st.number_input("Enter your budget (₹)", min_value=0)

# Recommend tourist spots
if st.button("Find Tourist Spots"):

    places = data[
        (data["location"] == location) &
        (data["category"] == interest) &
        (data["cost"] <= budget)]

    if len(places) > 0:
        st.subheader("Recommended Places")

        for _, place in places.iterrows():
            st.write("📍", place["name"])
            st.write("Cost: ₹", place["cost"])
            st.write(place["description"])
            st.write("---")
    else:
        st.warning("No matching places found.")
