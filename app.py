import streamlit as st
import requests
import os

# Foursquare API key
foursquare_api_key = os.environ.get("FOURSQUARE_API_KEY")

def get_coordinates(place_name):
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    headers = {
        'User-Agent': 'RealEstate/1.0 (adityak8340@gmail.com)'
    }

    try:
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            try:
                data = response.json()
                if data:
                    latitude = float(data[0]['lat'])
                    longitude = float(data[0]['lon'])
                    # Round to 2 decimal places
                    latitude = round(latitude, 2)
                    longitude = round(longitude, 2)
                    return latitude, longitude
                else:
                    st.warning("No data found for the specified place.")
                    return None
            except requests.exceptions.JSONDecodeError as e:
                st.error(f"JSON decode error: {e}")
                st.text("Response content:", response.text)
                return None
        else:
            st.error(f"Request failed with status code: {response.status_code}")
            st.text("Response content:", response.text)
            return None
    except requests.RequestException as e:
        st.error(f"Request error: {e}")
        return None

def get_nearby_projects(json_data):
    nearby_projects = []
    for result in json_data.get('results', []):
        project = {}
        project['name'] = result.get('name', 'Unknown')
        project['distance'] = result.get('distance', 'Unknown')
        project['categories'] = ', '.join(category['name'] for category in result.get('categories', []))
        project['address'] = result.get('location', {}).get('address', 'Unknown')
        project['postcode'] = result.get('location', {}).get('postcode', 'Unknown')
        project['country'] = result.get('location', {}).get('country', 'Unknown')
        project['developer_reputation'] = result.get('closed_bucket', 'Unknown')
        nearby_projects.append(project)
    return nearby_projects

# Streamlit UI
st.title("Real Estate Project Analysis")

place_name = st.text_input("Enter the name of the place:")
if st.button("Analyze"):
    coordinates = get_coordinates(place_name)
    if coordinates:
        st.write(f"Coordinates of {place_name}: ({coordinates[0]}, {coordinates[1]})")

        c = f"{coordinates[0]}%2C{coordinates[1]}"

        url = f"https://api.foursquare.com/v3/places/nearby?ll={c}&limit=50"

        headers = {
            "accept": "application/json",
            "Authorization": foursquare_api_key
        }

        response = requests.get(url, headers=headers)

        nearby_projects = get_nearby_projects(response.json())
        if nearby_projects:
            st.success("\nCompetitive Projects in the Vicinity:")
            for project in nearby_projects:
                st.write("\nName:", project["name"])
                st.write("Distance:", project["distance"], "m")
                st.write("Categories:", project["categories"])
                st.write("Address:", project["address"])
                st.write("Postcode:", project["postcode"])
                st.write("Country:", project["country"])
                st.write("Developer Reputation:", project["developer_reputation"])
        else:
            st.warning("No nearby projects found.")
    else:
        st.error("Failed to get coordinates.")
