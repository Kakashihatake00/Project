import requests

def get_mechanics_nearby(latitude, longitude, radius=5000):
    # Overpass API endpoint
    url = "http://overpass-api.de/api/interpreter"
    
    # Define the Overpass QL query
    query = f"""
    [out:json];
    (
      node["shop"="car_repair"](around:{radius},{latitude},{longitude});
      way["shop"="car_repair"](around:{radius},{latitude},{longitude});
      relation["shop"="car_repair"](around:{radius},{latitude},{longitude});
    );
    out center;
    """
    
    # Make the request to the API
    response = requests.get(url, params={'data': query})
    
    if response.status_code == 200:
        results = response.json().get('elements', [])
        if not results:
            print("No mechanics found nearby.")
            return []

        mechanics = []
        for element in results:
            if element['type'] == 'node':
                name = element.get('tags', {}).get('name', 'Unnamed mechanic')
                lat = element.get('lat')
                lon = element.get('lon')
                mechanics.append({
                    'name': name,
                    'latitude': lat,
                    'longitude': lon
                })
            elif element['type'] in ['way', 'relation']:
                name = element.get('tags', {}).get('name', 'Unnamed mechanic')
                center = element.get('center', {})
                lat = center.get('lat')
                lon = center.get('lon')
                mechanics.append({
                    'name': name,
                    'latitude': lat,
                    'longitude': lon
                })
        
        return mechanics
    else:
        print("Error making request:", response.status_code)
        return []

def display_mechanics(mechanics):
    if not mechanics:
        return
    for mechanic in mechanics:
        print(f"Name: {mechanic['name']}\nLatitude: {mechanic['latitude']}\nLongitude: {mechanic['longitude']}\n")

if __name__ == "__main__":
    # Get user location input
    try:
        USER_LATITUDE = float(input("Enter your latitude: "))
        USER_LONGITUDE = float(input("Enter your longitude: "))
    except ValueError:
        print("Invalid input. Please enter numeric values for latitude and longitude.")
        exit(1)

    mechanics = get_mechanics_nearby(USER_LATITUDE, USER_LONGITUDE)
    display_mechanics(mechanics)
