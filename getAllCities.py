import geonamescache

def get_cities_in_india():
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    india_cities = [city['name'] for city in gc.get_cities().values() if city['countrycode'] == 'IN']
    return india_cities

indian_cities = get_cities_in_india()
print(indian_cities)
print(len(indian_cities))