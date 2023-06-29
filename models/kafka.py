
import json





class Object:
    def __init__(self, no_plate, latitude, longitude):
        self.no_plate = no_plate
        self.latitude = latitude
        self.longitude = longitude

def create_kafka_objects(consumer):
    objects = []
    print('kafka consuming')
    while True:
        messages = consumer.poll(timeout_ms=1000)
        for tp, msgs in messages.items():
            for msg in msgs:
                data = json.loads(msg.value.decode('utf-8'))
                print (data,'kafka data')
                objects.append(data)
        consumer.commit()
        
        return objects





class Notification():
    def __init__(self,vehicle,destination,pickup_point,user_name):
        self.vehicle = vehicle
        self.destination = destination
        self.pickup_point = pickup_point
        self.user_name = user_name

def create_kafka_notifications(consumer):
    notifications = []
    print('notifications')
    while True:
        messages = consumer.poll(timeout_ms=10000)
        for tp, msgs in messages.items():
            for msg in msgs:
                data = json.loads(msg.value.decode('utf-8'))
                print (data,'notification kafka_data')
                notifications.append(data)
        consumer.commit()
        
        return notifications



