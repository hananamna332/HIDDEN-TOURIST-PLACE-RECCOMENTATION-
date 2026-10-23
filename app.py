
import streamlit as st
import requests

st.set_page_config(
    page_title="Hidden Tourist Finder",
    page_icon="🗺️"
)

st.title("🗺️ Hidden Tourist Place Recommendation")
st.write("Discover lesser-known destinations across India!")

# Store your API key in .streamlit/secrets.toml
API_KEY = st.secrets.get("GOOGLE_MAPS_API_KEY", "")

state = st.text_input(
    "Enter an Indian state",
    placeholder="Example: Kerala"
)

interest = st.selectbox(
    "What would you like to explore?",
    [
        "Nature and forests",
        "Waterfalls",
        "Hills and mountains",
        "Historical places",
        "Beaches and islands",
        "Caves and adventure",
        "Any type of hidden destination"
    ]
)

if st.button("Find Hidden Places"):
    if not API_KEY:
        st.error("Please configure your Google Maps API key.")
    elif not state.strip():
        st.warning("Please enter a state name.")
    else:
        query = (
            f"lesser-known tourist attractions for {interest} "
            f"in {state.strip()}, India"
        )

        url = "https://places.googleapis.com/v1/places:searchText"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": (
                "places.id,"
                "places.displayName,"
                "places.formattedAddress,"
                "places.rating,"
                "places.userRatingCount,"
                "places.googleMapsUri"
            )
        }

        payload = {
            "textQuery": query,
            "pageSize": 20,
            "regionCode": "IN",
            "languageCode": "en"
        }

        try:
            with st.spinner("Discovering destinations..."):
                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

            if response.status_code != 200:
                st.error(
                    f"Google Maps API error: "
                    f"{response.status_code}"
                )
                st.write(response.text[:1000])
            else:
                results = response.json().get("places", [])

                if not results:
                    st.info(
                        "No places found. Try another state "
                        "or travel interest."
                    )
                else:
                    # Rank places with fewer reviews first.
                    # This is only a rough hidden-gem signal.
                    results.sort(
                        key=lambda p: (
                            p.get("userRatingCount", 0),
                            -p.get("rating", 0)
                        )
                    )

                    st.subheader(
                        f"Recommendations for {state.strip()}"
                    )

                    for place in results[:10]:
                        name = place.get(
                            "displayName", {}
                        ).get("text", "Unnamed place")

                        address = place.get(
                            "formattedAddress",
                            "Address unavailable"
                        )

                        rating = place.get("rating")
                        reviews = place.get(
                            "userRatingCount", 0
                        )

                        map_url = place.get(
                            "googleMapsUri"
                        )

                        with st.container(border=True):
                            st.subheader("📍 " + name)
                            st.write("**Location:**", address)

                            if rating is not None:
                                st.write(
                                    f"⭐ Rating: {rating}/5"
                                )

                            st.write(
                                f"Review count: {reviews}"
                            )

                            if map_url:
                                st.link_button(
                                    "Open in Google Maps",
                                    map_url
                                )

                    st.caption(
                        "Recommendations are based on live "
                        "Google Places search results. A low "
                        "review count is only a rough indicator "
                        "of a lesser-known destination."
                    )

        except requests.RequestException as error:
            st.error(f"Could not connect: {error}")
