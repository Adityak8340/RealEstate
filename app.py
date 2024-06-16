import requests

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
                    latitude = data[0]['lat']
                    longitude = data[0]['lon']
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

# Example usage
place_name = "Eiffel Tower"
coordinates = get_coordinates(place_name)
if coordinates:
    print(f"Coordinates of {place_name}: ({coordinates[0]}, {coordinates[1]})")
else:
    print("Failed to get coordinates.")
