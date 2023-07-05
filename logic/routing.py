import requests
import os
from flask import flash

api_key=os.environ.get('google_api_key')
def get_distance(origin_lat, origin_lng, destination_lat, destination_lng):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': f'{origin_lat},{origin_lng}',
        'destination': f'{destination_lat},{destination_lng}',
        'key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception if the response is not successful
        data = response.json()

        if data['status'] == 'OK':
            distance = data['routes'][0]['legs'][0]['distance']['text']
            return distance
        else:
            return None

    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError) as e:
        print(f"Error: {e}")
        flash("No internet connection")



def calculate_route_distance(route):
    stages = route.stages  # Assuming 'stages' is a list of stage objects in the route
    longest_distance = 0.0

    for i in range(len(stages) - 1):
        stage1 = stages[i]
        stage2 = stages[i+1]
        print(stage1.latitude, stage1.longitude, 'for stage 1')
        print(stage2.latitude, stage2.longitude, 'for stage 2')
        distance_str = get_distance(stage1.latitude, stage1.longitude, stage2.latitude, stage2.longitude)
        distance = float(distance_str.split()[0])  # Extract the numeric part and convert to float
        print(distance, 'distance')
        if distance > longest_distance:
            longest_distance = distance

    return longest_distance




def reverse_geocode(latitude, longitude):
    # Replace YOUR_API_KEY with your actual API key

    # Define the API endpoint
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'

    # Make the HTTP request to the Geocoding API
    try:
        response = requests.get(url)
        data = response.json()
        

        # Parse the response to get the location name
        if data['status'] == 'OK':
            results = data['results']
            if results:
                location_name = results[0]['formatted_address']
                return location_name

        return None
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError) as e:
        print(f"Error: {e}")
        flash("No internet connection")


