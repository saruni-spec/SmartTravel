
from celery.result import AsyncResult
from kafka import KafkaConsumer, TopicPartition
from models.kafka import *

import sys
sys.path.append('/home/boss')



from celery import Celery

celery = Celery('myapp', broker='redis://localhost:6379/0')

# Optional configuration - If you have any additional Celery settings, you can define them here.
# For example:
# app.conf.update(
#     result_backend='redis://localhost:6379/0',
#     timezone='Europe/London',
# )






























def consume_notifications(consumer):
    notifications=create_kafka_notifications(consumer)
    print(notifications,'in ceelry')
    return notifications


def consume_notifications_task():
    consumer = KafkaConsumer(
    'booking_notification',
    group_id='notifications',
    bootstrap_servers=['localhost:9092'],
    consumer_timeout_ms=10000
)
    
    return consume_notifications(consumer)


from datetime import datetime, timedelta


def process_notifications():
    notifications_task = consume_notifications_task.apply_async(countdown=10)

    details = []
    consume_notifications_task_result = AsyncResult(notifications_task.id)
    consume_notifications_task_result.get()
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


def save_notifications(notifications,Notification):
    for notification in notifications:
        notification=Notification(notifications['vehicle'],notifications['rider'],notifications['timestamp'],notifications['pickup_point'],notifications['destination'])
        notification.save()


