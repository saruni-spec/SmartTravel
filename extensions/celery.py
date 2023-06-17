from celery import Celery
from kafka import KafkaConsumer, TopicPartition
from models.kafka import *

import sys
sys.path.append('/home/boss')




celery = Celery('extensions', broker='redis://localhost:6379/0')
celery.conf.result_backend = 'redis://localhost:6379/0'


print('running celery')



@celery.task
def consume_notifications(consumer):
    notifications=create_kafka_notifications(consumer)
    print(notifications,'in ceelry')
    return notifications

@celery.task
def consume_notifications_task():
    consumer = KafkaConsumer(
    'booking_notification',
    group_id='notifications',
    bootstrap_servers=['localhost:9092'],
    consumer_timeout_ms=10000,
    auto_offset_reset='earliest'
)
    partition = TopicPartition('booking_notification', 0)

# Assign the partition and seek to the beginning of the topic
    consumer.assign([partition])
    consumer.seek_to_beginning()
    return consume_notifications(consumer)


from datetime import datetime, timedelta

def process_notifications():
    notifications_task = consume_notifications_task.apply_async(countdown=10)

    details = []
    notifications_task.wait()
    current_time = datetime.now()
    # Check if the task has finished
    if notifications_task.ready():
        notifications = notifications_task.get()
        for notification in notifications:
            timestamp = datetime.strptime(notification['timestamp'], "%H:%M:%S")
            time_difference = current_time - timestamp
            
            # Check if the time difference is more than two minutes
            if time_difference > timedelta(minutes=2):
                details.append(notification)
    
    
    print(notifications, 'notifications in confirm booking')
    
    
    
    
    
    return details


class Notofications():

    def __init__(self,notifications):
        self.notifications=notifications
        

    def send_notification(self,notification):
        self.notifications.append(notification)

    @staticmethod
    def receive_notification(self,current_vehicle):
        current_time = datetime.now()
        for notification in self.notifications:
            if notification['vehicle']==current_vehicle:
                timestamp = datetime.strptime(notification['timestamp'], "%H:%M:%S")
                time_difference = current_time - timestamp
                if time_difference > timedelta(minutes=3):
                    print(notification,'sent to driver')

                    return notification
            else:
                return None
