import requests
api_key = 'AIzaSyA_JxBRmUKjcpPLWXwAagTX9k19tIWi2SQ'

def get_distance(origin_lat, origin_lng, destination_lat, destination_lng):
    # Replace YOUR_API_KEY with your actual API key
   

    # Define the API endpoint
    url = 'https://maps.googleapis.com/maps/api/directions/json'

    # Set up the parameters for the request
    params = {
        'origin': f'{origin_lat},{origin_lng}',
        'destination': f'{destination_lat},{destination_lng}',
        'key': api_key
    }

    # Make the HTTP request
    response = requests.get(url, params=params)
    data = response.json()

    # Parse the response to get the distance
    if data['status'] == 'OK':
        distance = data['routes'][0]['legs'][0]['distance']['text']
        return distance
    else:
        return None



def reverse_geocode(latitude, longitude):
    # Replace YOUR_API_KEY with your actual API key

    # Define the API endpoint
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'

    # Make the HTTP request to the Geocoding API
    response = requests.get(url)
    data = response.json()
    

    # Parse the response to get the location name
    if data['status'] == 'OK':
        results = data['results']
        if results:
            location_name = results[0]['formatted_address']
            return location_name

    return None



key3='AIzaSyAf1AH2Lh3Xh5nlSUlvnc5UWpAWib4MpFA'
key2='AIzaSyA_JxBRmUKjcpPLWXwAagTX9k19tIWi2SQ'
key1='AIzaSyAWYvsq4IwJAe-0p6kWv5pm20hj5BrIFvo'