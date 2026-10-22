
import streamlit as st
import requests

st.title("AI Tourist Spot Recommender")

location = st.text_input("Enter any city or place")

if st.button("Find Places"):

    if location:

        url = "https://nominatim.openstreetmap.org/search"

        response = requests.get(
            url,
            params={
                "q": location,
                "format": "json",
                "limit": 1 },  headers={"User-Agent": "TourismStudentProject"}, timeout=20 )

        data = response.json()

        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]

            query = f"""
            [out:json];
            node["tourism"="attraction"]
            (around:10000,{lat},{lon});
            out;
            """
            try:
                response = requests.post(
                    "https://overpass.kumi.systems/api/interpreter",
                    data={"data": query},
                    timeout=40)
                response.raise_for_status()
                result = response.json()
                results = result["elements"]

            except requests.RequestException:
                st.error("Tourist data is unavailable. Please try again later.")
                st.stop()

            
            st.subheader("Tourist Spots")

            count = 0

            for place in result["elements"]:
                name = place.get("tags", {}).get("name")

                if name:
                    st.write("📍", name)
                    count += 1

                if count == 10:
                    break

            if count == 0:
                st.write("No named attractions found.")

        else:
            st.write("Location not found.")

    else:
        st.write("Please enter a location.")
