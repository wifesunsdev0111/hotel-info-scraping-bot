from geopy.geocoders import Nominatim

def get_coordinates(location):
    geolocator = Nominatim(user_agent="my-app")  # Creating a geolocator object
    location = geolocator.geocode(location)  # Getting the location object
    latitude = location.latitude  # Extracting latitude
    longitude = location.longitude  # Extracting longitude
    return latitude, longitude

# # Example usage
# location = "Powai"
# latitude, longitude = get_coordinates(location)
# print(f"Latitude: {latitude}, Longitude: {longitude}")