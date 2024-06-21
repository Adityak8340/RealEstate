import streamlit as st
import requests
import os
from groq import Groq

# Setup API keys
foursquare_api_key = os.environ.get("FOURSQUARE_API_KEY")
openweathermap_api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
groq_api_key = os.environ.get("GROQ_API_KEY")

# Set up the Groq client
client = Groq(api_key=groq_api_key)

def get_coordinates(place_name):
    url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
    headers = {
        'User-Agent': 'RealEstate/1.0 (adityak8340@gmail.com)'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                latitude = round(float(data[0]['lat']), 2)
                longitude = round(float(data[0]['lon']), 2)
                return latitude, longitude
            else:
                st.warning("No data found for the specified place.")
                return None
        else:
            st.error(f"Request failed with status code: {response.status_code}")
            st.text(response.text)
            return None
    except requests.RequestException as e:
        st.error(f"Request error: {e}")
        return None

def get_nearby_projects(json_data):
    nearby_projects = []
    for result in json_data.get('results', []):
        project = {
            'name': result.get('name', 'Unknown'),
            'distance': result.get('distance', 'Unknown'),
            'categories': ', '.join(category['name'] for category in result.get('categories', [])),
            'address': result.get('location', {}).get('address', 'Unknown'),
            'postcode': result.get('location', {}).get('postcode', 'Unknown'),
            'country': result.get('location', {}).get('country', 'Unknown'),
            'developer_reputation': result.get('closed_bucket', 'Unknown')
        }
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
            st.text(response.text)
            return None
    except requests.RequestException as e:
        st.error(f"Request error: {e}")
        return None

def get_nearby_facilities(lat, lon, categories):
    facilities = []
    for category in categories:
        url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&categories={category}&limit=10"
        headers = {
            "accept": "application/json",
            "Authorization": foursquare_api_key
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                facilities.extend(response.json().get('results', []))
            else:
                st.error(f"Failed to get nearby facilities. Status code: {response.status_code}")
                st.text(response.text)
        except requests.RequestException as e:
            st.error(f"Request error: {e}")
    return facilities

def display_facilities(facilities, facility_type):
    if facilities:
        st.write(f"\nNearby {facility_type.capitalize()}:")
        for facility in facilities:
            col1, col2 = st.columns([2, 1])
            with col1:
                name = facility.get('name', 'Unknown')
                st.write(f"- {name}")
            with col2:
                distance = facility.get('distance', 'Unknown')
                st.write(f"({distance} m away)")
    else:
        st.write(f"No nearby {facility_type} found.")

def generate_response(user_prompt, text_content):
    try:
        # Define the system prompt with strict attribute order and an example
        system_prompt = (
            "You help with Real Estate Project Analysis. Given a main project and its competitors, you need to analyze the competitive projects. "
            "You also need to provide information about the air quality and nearby facilities. "
            "Make logical reasoning for comparing projects, and tell which one will be the best project with grades for each project. "
            "You generate a report table with the analysis and reasoning."
        )

        # Concatenate the system and user prompts
        prompt = f"{system_prompt}\n\nDocument Text: {text_content}\n\nUser Query: {user_prompt}\n\nAnswer:"

        # Call the Groq model with the combined prompt
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Document Text: {text_content}\n\nUser Query: {user_prompt}"}
            ],
            model="llama3-8b-8192",
        )

        # Get the chatbot's response
        chatbot_response = "🤖:" + chat_completion.choices[0].message.content.strip()

        return chatbot_response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return {}

def analyze_projects(main_project_name, main_project_aqi, projects):
    project_details = "\n".join([
        f"Name: {project['name']}\nDistance: {project['distance']} m\nCategories: {project['categories']}\n"
        f"Address: {project['address']}\nPostcode: {project['postcode']}\nCountry: {project['country']}\n"
        f"Developer Reputation: {project['developer_reputation']}\nAir Quality Index (AQI): {project.get('aqi', 'Unknown')}\n"
        f"Nearby Facilities:\n    " + "\n    ".join([f"{facility.get('name', 'Unknown')} ({facility.get('distance', 'Unknown')} m away)" for facility in project.get('facilities', [])])
        for project in projects
    ])

    text_content = f"Main Project Name: {main_project_name}\nAir Quality Index (AQI): {main_project_aqi}\n\nCompetitive Projects:\n{project_details}"
    user_query = "Compare the main project with the competitive projects and determine which is the best. Provide reasoning and grades for each project."

    return generate_response(user_query, text_content)

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
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write("\nName:", project["name"])
                with col2:
                    st.write("Distance:", project["distance"], "m")
                with col3:
                    st.write("Categories:", project["categories"])
                with col4:
                    st.write("Address:", project["address"])
                st.write("Postcode:", project["postcode"])
                st.write("Country:", project["country"])
                st.write("Developer Reputation:", project["developer_reputation"])

                proj_coordinates = get_coordinates(project["name"])
                if proj_coordinates:
                    air_quality = get_air_quality(proj_coordinates[0], proj_coordinates[1])
                    if air_quality:
                        aqi = air_quality["list"][0]["main"]["aqi"]
                        project["aqi"] = aqi
                        st.write(f"Air Quality Index (AQI) for {project['name']}: {aqi}")
                    else:
                        st.warning(f"Could not retrieve air quality data for {project['name']}.")

                    # Get and display nearby facilities
                    categories = ['13018', '13065', '17067', '18025', '18037']
                    facilities = get_nearby_facilities(proj_coordinates[0], proj_coordinates[1], categories)
                    project["facilities"] = facilities
                    display_facilities(facilities, 'facilities')
                else:
                    st.warning(f"Could not retrieve coordinates for {project['name']}.")
        else:
            st.warning("No competitive real estate projects found.")

        air_quality = get_air_quality(coordinates[0], coordinates[1])
        if air_quality:
            st.success("Current Air Quality Data for Main Project:")
            aqi = air_quality["list"][0]["main"]["aqi"]
            st.write(f"Air Quality Index (AQI): {aqi}")

            response_text = analyze_projects(place_name, aqi, nearby_projects)
            st.write(response_text, unsafe_allow_html=True)
        else:
            st.error("Could not retrieve air quality data for the main project.")
    else:
        st.error("Failed to get coordinates.")
