from .celery import celery
from flask import Blueprint, request, session,redirect
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required, current_user
from kafka import KafkaProducer,KafkaConsumer
import json
from models.vehicle import Vehicle
from logic.routing import *
from datetime import datetime
from flask import url_for



producer = KafkaProducer(bootstrap_servers='localhost:9092')
bp = Blueprint('tracker', __name__)

@bp.route('/tracker/track', methods=['GET', 'POST'])
@login_required
def track_user():
    user_name = current_user.user_name
    print(user_name,'tracking user_name')
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
        session['tracking_coordinates'] = {'latitude':latitude,'longitude': longitude}
        if is_driver == True:
            vehicle=Vehicle.query.filter_by(driver_username=user_name).first()
            
            current_vehicle=vehicle.no_plate
            tracking_details = {"vehicle": current_vehicle, "latitude": latitude, "longitude": longitude,'timestamp':time}
            print(tracking_details,'tracking_details driver')
            if vehicle.vehicle_type=='bus':
                docked=session.get('docked',None)
                
                if docked:
                    
                    tracking_details['bus_destination']=session.get('bus_destination',None)
                    tracking_details['docked']=docked
                    tracking_details['docking_stage']=session.get('docking_stage',None)
                else:
                    tracking_details['docked']=False
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
    return redirect(url_for('index.index'))
    

@celery.task(bind=True)
def start_tracking():
    track_user()



@bp.route('/tracker/destination', methods=['GET', 'POST'])
@login_required
def reach_destination():
    import time
    tolerance = 0.005  # Adjust the tolerance level as needed
    destination_coordinates = session.get('destination_coordinates')
    print('it is ineveitable')
    while True:
        current_coordinates = session.get('tracking_coordinates')
        if current_coordinates is not None:
            current_lat = current_coordinates.get('latitude')
            current_lon = current_coordinates.get('longitude')

            lat_diff = abs(float(current_lat) - float(destination_coordinates['latitude']))
            lon_diff = abs(float(current_lon) - float(destination_coordinates['longitude']))

            if lat_diff <= tolerance and lon_diff <= tolerance:
                session['arrived'] = True
                return "success"
            else:
                session['arrived'] = False
                print('not arrived')
        
        time.sleep(60)

@celery.task
def start_routing():
    reach_destination()
    


@bp.route('/profile/driver/capacity', methods=['GET', 'POST'])
@login_required
def book_vehicle():
    from flask import jsonify
    import time
    vehicle_plate=session.get('my_vehicle',None)
    vehicle=Vehicle.query.filter_by(no_plate=vehicle_plate).first()
    
    capacity=vehicle.check_availability()
    if capacity<=2:
        vehicle.stop_bookings()

    
    return jsonify({'capacity': capacity})   


@celery.task
def start_booking():
    book_vehicle ()