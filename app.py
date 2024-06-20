import streamlit as st
import requests
import os

# Foursquare API key and OpenWeatherMap API key
foursquare_api_key = os.environ.get("FOURSQUARE_API_KEY")
openweathermap_api_key = os.environ.get("OPENWEATHERMAP_API_KEY")

def get_coordinates(place_name):
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    headers = {
        'User-Agent': 'RealEstate/1.0 (adityak8340@gmail.com)'
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data:
                    latitude = float(data[0]['lat'])
                    longitude = float(data[0]['lon'])
                    latitude = round(latitude, 2)
                    longitude = round(longitude, 2)
                    return latitude, longitude
                else:
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
        if 'Residential Building' in project['categories']:
            nearby_projects.append(project)
    return nearby_projects

def get_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={openweathermap_api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get air quality data. Status code: {response.status_code}")
            st.text("Response content:", response.text)
            return None
    except requests.RequestException as e:
        st.error(f"Request error: {e}")
        return None

# Streamlit UI
st.title("Real Estate Project Analysis")

place_name = st.text_input("Enter the name of the main project:")
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
            st.success("\nCompetitive Real Estate Projects in the Vicinity:")
            for project in nearby_projects:
                st.write("\nName:", project["name"])
                st.write("Distance:", project["distance"], "m")
                st.write("Categories:", project["categories"])
                st.write("Address:", project["address"])
                st.write("Postcode:", project["postcode"])
                st.write("Country:", project["country"])
                st.write("Developer Reputation:", project["developer_reputation"])

                proj_coordinates = get_coordinates(project["name"])
                if proj_coordinates:
                    air_quality = get_air_quality(proj_coordinates[0], proj_coordinates[1])
                    if air_quality:
                        aqi = air_quality["list"][0]["main"]["aqi"]
                        st.write(f"Air Quality Index (AQI) for {project['name']}: {aqi}")
                    else:
                        st.warning(f"Could not retrieve air quality data for {project['name']}.")
                else:
                    st.warning(f"Could not retrieve coordinates for {project['name']}.")
            
        else:
            st.warning("No competitive real estate projects found.")

        air_quality = get_air_quality(coordinates[0], coordinates[1])
        if air_quality:
            st.success("Current Air Quality Data for Main Project:")
            aqi = air_quality["list"][0]["main"]["aqi"]
            st.write(f"Air Quality Index (AQI): {aqi}")
        else:
            st.error("Could not retrieve air quality data for the main project.")
    else:
        st.error("Failed to get coordinates.")
