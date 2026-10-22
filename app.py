
import streamlit as st
import requests

st.title("AI Tourist Spot Recommender")

location = st.text_input("Enter any city or place")

if st.button("Find Tourist Spots"):

    if not location.strip():
        st.warning("Please enter a location.")

    else:
        try:
            # Find the location
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": location,
                    "format": "json",
                    "limit": 1
                },
                headers={"User-Agent": "TouristProject/1.0"},
                timeout=20
            )
            response.raise_for_status()
            data = response.json()

            if not data:
                st.error("Location not found.")

            else:
                lat = data[0]["lat"]
                lon = data[0]["lon"]

                # Find nearby attractions
                query = f"""
                [out:json][timeout:25];
                nwr["tourism"="attraction"]
                (around:10000,{lat},{lon});
                out center tags;
                """

                response = requests.post(
                    "https://overpass-api.de/api/interpreter",
                    data={"data": query},
                    timeout=40
                )
                response.raise_for_status()
                places = response.json()["elements"]

                st.subheader("Tourist Spots")
                count = 0

                for place in places:
                    name = place.get("tags", {}).get("name")

                    if name:
                        st.write("📍", name)
                        count += 1

                    if count == 10:
                        break

                if count == 0:
                    st.info("No named attractions found.")

        except (requests.RequestException, ValueError, KeyError):
            st.error(
                "Search is unavailable. Please try again later."
            )
