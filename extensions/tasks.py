from .celery import celery
from flask import Blueprint, request, session
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required, current_user
from kafka import KafkaProducer,KafkaConsumer
import json
from models.vehicle import Vehicle
from logic.routing import *
from datetime import datetime



producer = KafkaProducer(bootstrap_servers='localhost:9092')
bp = Blueprint('tracker', __name__)

@bp.route('/tracker/track', methods=['GET', 'POST'])
@login_required
def track_user():
    user_name = current_user.user_name
    is_driver=current_user.check_if_driver()
    if request.method == 'POST':
        time=datetime.now().strftime("%H:%M:%S")
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError:
            error = "Invalid CSRF token"
            print(error,'error')
            return error,400
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        if is_driver == True:
            vehicle=Vehicle.query.filter_by(driver_username=user_name).first()
            current_vehicle=vehicle.no_plate
            tracking_details = {"vehicle": current_vehicle, "latitude": latitude, "longitude": longitude,'timestamp':time}
            print(tracking_details,'tracking_details driver')
            if vehicle.vehicle_type=='bus':
                message = json.dumps(tracking_details)
                producer.send('bus_coordinates', value=message.encode())
            elif vehicle.vehicle_type=='taxi':
                message = json.dumps(tracking_details)
                producer.send('taxi_coordinates', value=message.encode())
            else:
                message = json.dumps(tracking_details)
                producer.send('hybrid_coordinates', value=message.encode())
        else:
            tracking_details = {"username": user_name, "latitude": latitude, "longitude": longitude,'timestamp':time}
            print(tracking_details,'tracking_details rider')
            message = json.dumps(tracking_details)
            producer.send('user_coordinates', value=message.encode())
    
        session['current_location'] = tracking_details

        

       
        location_name = reverse_geocode(session.get('current_location').get('latitude'), session.get('current_location').get('longitude'))
        session['location_name']=location_name
        return "success"
    

@celery.task(bind=True)
def start_tracking():
    track_user()










