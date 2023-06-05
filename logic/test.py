import math
from sklearn.cluster import KMeans
from models.stages import  Stages

def calculate_distance(lat1,long1,lat2,long2):
    lat1_rad=math.radians(lat1)
    lat2_rad=math.radians(lat2)
    long1_rad=math.radians(long1)
    long2_rad=math.radians(long2)

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
            bus_stop_lat = bus_stop['latitude']
            bus_stop_lon = bus_stop['longitude']
            distance = calculate_distance(user_lat, user_lon, bus_stop_lat, bus_stop_lon)
            
            if distance < closest_distance:
                closest_distance = distance
                closest_bus_stop = bus_stop
    
    return closest_bus_stop


def group_coordinates(coordinates, num_clusters):
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    points = [[coord.latitude,coord.longitude] for coord in coordinates]
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



stages_data = Stages.Query.all()

stage_clusters=group_coordinates(stages_data, 5)
print(find_closest_bus_stop(-1.1781268, 36.9364686, stage_clusters))
