from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geopy.geocoders

geopy.geocoders.options.default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def get_lat_lng(address):
    geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    try:
        location = geolocator.geocode(address)
        if location:
            lat = location.latitude
            lng = location.longitude
            return lat, lng
    except GeocoderTimedOut:
        return get_lat_lng(address)  # Retry if geocoding times out
    return None

# Example usage
address = '1600 Amphitheatre Parkway, Mountain View, CA'
coordinates = get_lat_lng(address)
if coordinates:
    lat, lng = coordinates
    print(f'Latitude: {lat}, Longitude: {lng}')
else:
    print('Failed to geocode the address.')