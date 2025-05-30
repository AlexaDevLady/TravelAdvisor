from pymongo import MongoClient
import requests

# MongoDB setup
client = MongoClient('mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # 🔁 Replace with your actual Mongo URI
db = client['travel_blog']
destinations_col = db['destinations']

# Geocoding API (OpenCageData is recommended for ease)
GEOCODE_API_KEY = 'd77c8e33b0ea408285dbe35b835d3ed4'

def fetch_coordinates(city_name):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={GEOCODE_API_KEY}'
    res = requests.get(url).json()
    if res['results']:
        lat = res['results'][0]['geometry']['lat']
        lon = res['results'][0]['geometry']['lng']
        return lat, lon
    return None, None

def update_destinations():
    for dest in destinations_col.find():
        if 'lat' not in dest or 'lon' not in dest:
            lat, lon = fetch_coordinates(dest['name'])
            if lat and lon:
                destinations_col.update_one(
                    {'_id': dest['_id']},
                    {'$set': {'lat': lat, 'lon': lon}}
                )
                print(f"Updated {dest['name']} with lat={lat}, lon={lon}")
            else:
                print(f"Failed to get coordinates for {dest['name']}")

if __name__ == '__main__':
    update_destinations()
