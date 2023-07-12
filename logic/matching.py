import math
from sklearn.cluster import KMeans
import numpy as np
import requests
from .routing import *


def get_time(origin_location, destination_location, travel_mode, api_key):
    print(origin_location,'origin location')
    print(destination_location,'destination location')
    print(travel_mode,'travel mode')
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_location}&destination={destination_location}&mode={travel_mode}&key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'OK':
            route = data['routes'][0]
            leg = route['legs'][0]
            duration = leg['duration']['text']
            print(duration,'duration')
            return duration
        else:
            return None
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError) as e:
        print(f"Error: {e}")
        flash("No internet connection")


def calculate_distance(lat1,long1,lat2,long2):
    lat1_rad=math.radians(float(lat1))
    lat2_rad=math.radians(float(lat2))
    long1_rad=math.radians(float(long1))
    long2_rad=math.radians(float(long2))

    dlon = long2_rad - long1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c  # Earth's radius in kilometers
    return distance

def find_closest_bus_stop(user_lat, user_lon, bus_stops):
    if bus_stops is None:  # Check if bus_stops is None
        return None
    
    closest_distance = float('inf')
    closest_bus_stop = None

    for cluster_label, bus_stops_list in bus_stops.items():
        for bus_stop in bus_stops_list:
            bus_stop_lat = bus_stop['latitude']
            bus_stop_lon = bus_stop['longitude']
            
            distance = calculate_distance(user_lat, user_lon, bus_stop_lat, bus_stop_lon)
            
            if distance < closest_distance:
                closest_distance = distance
                closest_bus_stop = bus_stop
    
    return closest_bus_stop

def find_closest_bus(user_lat, user_lon, bus_stops,user_distance):
    if bus_stops is None :  # Check if bus_stops is None
        return None
    
    
    closest_distance = float('inf')
    closest_bus_stop = None

    for cluster_label, bus_stops_list in bus_stops.items():
        for bus_stop in bus_stops_list:
            bus_stop_lat = bus_stop['latitude']
            bus_stop_lon = bus_stop['longitude']
            distance = calculate_distance(user_lat, user_lon, bus_stop_lat, bus_stop_lon)
            if distance >float( user_distance.split()[0]):
                if distance < closest_distance:
                    closest_distance = distance
                    closest_bus_stop = bus_stop
                    
    
    return closest_bus_stop


def group_coordinates(coordinates, num_clusters):
    if not coordinates or len(coordinates) == 0:  # Check if coordinates list is empty
        return None
    # Perform K-means clustering
    if len(coordinates) < num_clusters:
        num_clusters = len(coordinates)

    
    kmeans = KMeans(n_clusters=num_clusters)
    points = np.array ([[coord['latitude'],coord['longitude']] for coord in coordinates])
    kmeans.fit(points)

    # Get the cluster labels for each coordinate
    labels = kmeans.labels_

    # Assign each coordinate to its corresponding cluster
    clusters = {}
    for i, coord in enumerate(coordinates):
        cluster_label = labels[i]
        if cluster_label not in clusters:
            clusters[cluster_label] = []
        clusters[cluster_label].append(coord)

    return clusters


            
def find_bus( bus_cluster,stage_location,user_time):
    if bus_cluster is None:  # Check if bus_stops is None
        return None
    closest_buses = []

    for cluster_label, bus_list in bus_cluster.items():
        for bus in bus_list:
            bus_lat = bus['latitude']
            bus_lon = bus['longitude']
            location=reverse_geocode(bus_lat,bus_lon)
            bus_time=get_time(location,stage_location[0]['stage_name'],'driving',api_key)
            
            if bus_time>user_time:
                    closest_buses.append(bus)
                    

    return closest_buses


def create_stage_dict(stages):
    Data=[]
    for stage in stages:
        stage_data={
        'stage_no':stage.stage_no,
        'latitude':stage.latitude,
        'longitude':stage.longitude,
        'stage_name':stage.stage_name,
        'stage_description':stage.stage_description}
        Data.append(stage_data)
    return Data

from datetime import datetime

def get_direction(vehicle_data, destination):
    if vehicle_data is None or len(vehicle_data)==0:  # Check if bus_stops is None
        return None
    bus_group = []
    for bus in vehicle_data:
            print(bus,'bus in get distance')
            bus_id = bus['vehicle']
            distance_to_destination = calculate_distance(destination['latitude'], destination['longitude'], bus['latitude'], bus['longitude'])
            bus_timestamp = datetime.strptime(bus['timestamp'], "%H:%M:%S")
            for other_bus in vehicle_data:
                if bus_id == other_bus['vehicle'] and bus is not other_bus:
                    other_bus_timestamp = datetime.strptime(other_bus['timestamp'], "%H:%M:%S")
                    if bus_timestamp > other_bus_timestamp:
                        other_bus_distance = calculate_distance(destination['latitude'], destination['longitude'], other_bus['latitude'], other_bus['longitude'])
                        if distance_to_destination < other_bus_distance:
                            if bus not in bus_group:
                                bus_group.append(bus)
    return bus_group

def docked_buses(user_destination,bus_details):
    docked_buses=[]
    if bus_details is None or len(bus_details)==0:  # Check if bus_stops is None
        return None
    else:
        for bus in bus_details:
            if bus['docked']:
                if bus['destination']==user_destination:
                    docked_buses.append(bus)




def find_closest_bus_stop_to_bus(user_lat, user_lon, bus_stops):
    if bus_stops is None or len(bus_stops)==0:  # Check if bus_stops is None
        return None
    
    closest_distance = float('inf')
    closest_bus_stop = None

    
    for bus_stop in bus_stops:
        bus_stop_lat = bus_stop.latitude
        bus_stop_lon = bus_stop.longitude
        
        distance = calculate_distance(user_lat, user_lon, bus_stop_lat, bus_stop_lon)
        
        if distance < closest_distance:
            closest_distance = distance
            closest_bus_stop = bus_stop

    return closest_bus_stop

def find_route(bus_data):
    if bus_data is None or len(bus_data)==0:
        return None
    else:
        print(bus_data,'bus data in find route')
        
        from models.routes import Route
        routes=Route.query.all()
        for bus in bus_data:
            if bus['docked']:
                
                current_stage=bus['docking_stage']
                destination=bus['bus_destination']
                viable_routes=[]
                for route in routes:
                    for stage in route.stages:
                       
                        if stage.stage_name==current_stage:
                           
                            condition1=True
                    for another_stage in route.stages:
                        
                        if another_stage.stage_name==destination:
                            
                            condition2=True
                    if condition1 and condition2:
                        viable_routes.append(route)
            if viable_routes is None or len(viable_routes)==0:
                return None
            else:
                print (viable_routes,'viable routes in find route')
                shortest_route=viable_routes[0]
                for route in viable_routes:
                    print(route,'route in find route')
                    print(route.stages,'route stages in find route')
                    print(route.route_distane,'route distane in find route')
                    if route.route_distane<=shortest_route.route_distane:
                        shortest_route=route
        
                bus['shortest_route']={'id':shortest_route.id,'distance':shortest_route.route_distane}
    return bus_data
    
def allow_passenger(bus_data,passenger_destination,nearest_stage):
    from models.routes import Route
    if bus_data is None:
        return None
    else:

        viable_buses=[]
        for bus in bus_data:
            if bus['docking_stage']==nearest_stage:
                route_id=bus['shortest_route']['id']
                route=Route.query.filter_by(id=route_id).first()
                stages=route.stages
                for stage in stages:
                    if stage.stage_name==passenger_destination:
                        viable_buses.append(bus)
                    
        return viable_buses
    

def find_closest_hybrid_to_stage(stage_lat, stage_lon,hybrids):
    if hybrids is None or len(hybrids)==0:  # Check if bus_stops is None
        return None
    
    closest_distance = float('inf')
    closest_hybrid = None

    
    for hybrid in hybrids:
        hybrid_lat = hybrid['latitude']
        hybrid_lon = hybrid['longitude']
        
        distance = get_distance(stage_lat, stage_lon, hybrid_lat, hybrid_lon)
        
        if distance < closest_distance:
            closest_distance = distance
            closest_hybrid = hybrid

    return closest_hybrid



notifications=[]
from datetime import datetime, timedelta
def receive_notification(notifications ,current_vehicle):
        current_notifiations=[]
        current_time = datetime.now()
        for notification in notifications:
            if notification['vehicle']==current_vehicle:
                timestamp = datetime.strptime(notification['timestamp'], "%H:%M:%S")
                time_difference = current_time - timestamp
                if time_difference > timedelta(minutes=3):
                    print(notification,'sent to driver')
                    current_notifiations.append(notification)
            
                
        return current_notifiations 