
from kafka import KafkaConsumer
from models.kafka import *



@celery.task
def consume_notifications(consumer):
    notifications=create_kafka_notifications(consumer)
    return notifications

@celery.task
def consume_notifications_task():
    consumer_notification = KafkaConsumer('booking_notification',group_id='notifications',bootstrap_servers=['localhost:9092'],consumer_timeout_ms=10000) 
    consume_notifications(consumer_notification)



