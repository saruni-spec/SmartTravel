
import json





class Object:
    def __init__(self, no_plate, latitude, longitude):
        self.no_plate = no_plate
        self.latitude = latitude
        self.longitude = longitude

def create_kafka_objects(consumer):
    objects = []
    print('objectify')
    while True:
        messages = consumer.poll(timeout_ms=1000)
        for tp, msgs in messages.items():
            for msg in msgs:
                data = json.loads(msg.value.decode('utf-8'))
                print (data,'data')
                object = Object(data['vehicle'], data['latitude'], data['longitude'])
                objects.append(object)
                print(f"Received message: {msg.value}")
        consumer.commit()
        
        return objects

print("here")



