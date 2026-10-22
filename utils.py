import requests

def find_location(location):
    url = "https://nominatim.openstreetmap.org/search"

    response = requests.get(
        url,
        params={"q": location, "format": "json", "limit": 1},
        headers={"User-Agent": "TourismStudentProject"},
        timeout=20
    )

    response.raise_for_status()
    places = response.json()

    if places:
        return places[0]["lat"], places[0]["lon"]

    return None
