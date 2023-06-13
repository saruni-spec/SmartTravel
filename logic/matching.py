import math
from sklearn.cluster import KMeans
import numpy as np


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
    closest_distance = float('inf')
    closest_bus_stop = None

    for cluster_label, bus_stops_list in bus_stops.items():
        for bus_stop in bus_stops_list:
            bus_stop_lat = bus_stop.latitude
            bus_stop_lon = bus_stop.longitude
            distance = calculate_distance(user_lat, user_lon, bus_stop_lat, bus_stop_lon)
            
            if distance < closest_distance:
                closest_distance = distance
                closest_bus_stop = bus_stop
    
    return closest_bus_stop

def find_closest_bus(user_lat, user_lon, bus_stops,user_distance):
    closest_distance = float('inf')
    closest_bus_stop = None

    for cluster_label, bus_stops_list in bus_stops.items():
        for bus_stop in bus_stops_list:
            bus_stop_lat = bus_stop.latitude
            bus_stop_lon = bus_stop.longitude
            distance = calculate_distance(user_lat, user_lon, bus_stop_lat, bus_stop_lon)
            if distance >float( user_distance.split()[0]):
                if distance < closest_distance:
                    closest_distance = distance
                    closest_bus_stop = bus_stop
                    
    
    return closest_bus_stop


def group_coordinates(coordinates, num_clusters):
    # Perform K-means clustering
    if len(coordinates) < num_clusters:
        num_clusters = len(coordinates)

    
    kmeans = KMeans(n_clusters=num_clusters)
    points = np.array ([[coord.latitude,coord.longitude] for coord in coordinates])
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



def find_bus( bus_stops,user_destination,bus_location,user_time,bus_time):
    closest_bus_stop = None
    

    for cluster_label, bus_stops_list in bus_stops.items():
        for bus_stop in bus_stops_list:
            bus_stop_lat = bus_stop.latitude
            bus_stop_lon = bus_stop.longitude
            if bus_time>user_time:
                    distance_to_detination=calculate_distance(user_destination['latitude'], user_destination['longitude'],bus_stop_lat, bus_stop_lon)
                    new_distance=calculate_distance(user_destination['latitude'], user_destination['longitude'],bus_location['latitude'], bus_location['longitude'])
                    if new_distance<distance_to_detination:
                        closest_bus_stop = bus_stop

    return closest_bus_stop


