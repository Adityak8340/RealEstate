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
                    print("No data found for the specified place.")
                    return None
            except requests.exceptions.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print("Response content:", response.text)
                return None
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response content:", response.text)
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
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

# Example usage
place_name = "Purva Westend"
coordinates = get_coordinates(place_name)
if coordinates:
    print(f"Coordinates of {place_name}: ({coordinates[0]}, {coordinates[1]})")

    c = f"{coordinates[0]}%2C{coordinates[1]}"

    url = f"https://api.foursquare.com/v3/places/nearby?ll={c}&limit=50"

    headers = {
        "accept": "application/json",
        "Authorization": foursquare_api_key
    }

    response = requests.get(url, headers=headers)

    print(response.text)

    nearby_projects = get_nearby_projects(response.json())
    if nearby_projects:
        print("\nCompetitive Projects in the Vicinity:")
        for project in nearby_projects:
            print("\nName:", project["name"])
            print("Distance:", project["distance"], "m")
            print("Categories:", project["categories"])
            print("Address:", project["address"])
            print("Postcode:", project["postcode"])
            print("Country:", project["country"])
            print("Developer Reputation:", project["developer_reputation"])
    else:
        print("No nearby projects found.")
else:
    print("Failed to get coordinates.")
