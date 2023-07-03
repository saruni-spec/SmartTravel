
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




def remove_duplicate_notifications(notifications, lst):
    for notification in notifications[:]:
        rider = notification['rider']
        for item in lst:
            if rider == item['rider']:
                while notification in notifications:
                    notifications.remove(notification)
                break
def check_notifications(notifications,no_plate,notification_list):
    from datetime import datetime,timedelta
    
    count=0
    
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    date = datetime.strptime(date_str, "%Y-%m-%d")


    time_str = datetime.now().strftime("%H:%M:%S")
    time = datetime.strptime(time_str, "%H:%M:%S")

    print(notifications,'in check notifications')
    if notifications is None or len(notifications)==0:
        return notification_list
    
    else:
        for notification in notifications:
            print(notification['vehicle'],'notification vehicle ')
            print(no_plate,'no plate for comoarison')
            if notification['vehicle']==no_plate:
                
                today = datetime.strptime(notification['date'], "%Y-%m-%d")
                print(today,'today')
                print(date,'date in comparison')
                if today==date:
                    timestamp = datetime.strptime(notification['timestamp'], "%H:%M:%S")
                    time_difference = time - timestamp
                    print(time_difference,'time difference in check notifications')
                    if time_difference < timedelta(minutes=10):
                        if len(notification_list)!=0:
                            print(notification_list,'notification_list not empty')
                            
                            for message in notification_list:
                                if message['booking_id']==notification['booking_id']:
                                    print('message exits')
                                else:
                                    print('message not exits')
                                    notification_list.append(notification)
                                    count=count+1
                        else:
                            notification_list.append(notification)
                            count=count+1
    return [notification_list,count]