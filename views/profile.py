from flask import render_template, Blueprint, request, session,redirect
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required,current_user
from logic.routing import *
from kafka import KafkaProducer
import json
from functools import wraps
from models.owner import Owner
from models.driver import Driver
from extensions.extensions import db



def is_driver(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            driver = Driver.query.filter_by(user_name=current_user.user_name).first()
            if not driver:
                # Redirect or return an error message if user is not a driver
                return "Unauthorized: Access denied for non-drivers"
            return func(*args, **kwargs)
        return wrapper

def is_owner(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        owner = Owner.query.filter_by(user_name=current_user.user_name).first()
        if not owner:
            # Redirect or return an error message if user is not an owner
            return "Unauthorized: Access denied for non owners"
        return func(*args, **kwargs)
    return wrapper



producer = KafkaProducer(bootstrap_servers='localhost:9092')

bp = Blueprint('profile', __name__) 


@bp.route('/profile/rider', methods=['GET', 'POST'])
@login_required
def rider():
    user_name=current_user.user_name
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        session['current_location'] = {"username":user_name,"latitude": latitude, "longitude": longitude}
        
        message = json.dumps({"username":user_name,"latitude": latitude, "longitude": longitude})
        producer.send('user_coordinates', value=message.encode())
        
    

    else:
        
        if session.get('current_location')  is None:
            location_name = ""
        else:
            location_name = reverse_geocode(session.get('current_location').get('latitude'), session.get('current_location').get('longitude'))
            session['location_name']=location_name
        return render_template('profile_rider.html',user_name=user_name,current_location=location_name)



    
    return render_template('profile_rider.html')
            

@bp.route('/profile/owner', methods=['GET', 'POST'])
@login_required
@is_owner
def profile_owner():
    user_name=current_user.user_name
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
        
        print(user_name,'owner')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        session['current_location'] = {'owner':user_name,"latitude": latitude, "longitude": longitude}
        message = json.dumps({'owner':user_name,"latitude": latitude, "longitude": longitude})
        producer.send('owner_coordinates', value=message.encode())
        
    else:
        if session.get('current_location')  is None:
            location_name = ""
        else:
            location_name = reverse_geocode(session.get('current_location').get('latitude'), session.get('current_location').get('longitude'))
            session['location_name']=location_name
        return render_template('profile_owner.html',user_name=user_name,current_location=location_name)
    


    return render_template('profile_owner.html')




@bp.route('/profile/driver', methods=['GET', 'POST'])
@login_required
@is_driver
def profile_driver():
    from models.vehicle import Vehicle
    user_name=current_user.user_name
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        vehicle=Vehicle.query.filter_by(driver_username=user_name).first()
        current_vehicle=vehicle.no_plate
        print(current_vehicle,':',latitude, 'latitude',longitude, 'longitude')
        session['current_location'] = {'vehicle':current_vehicle,"latitude": latitude, "longitude": longitude}
        message = json.dumps({'vehicle':current_vehicle,"latitude": latitude, "longitude": longitude})
        producer.send('bus_coordinates', value=message.encode())
        

    else:
        if session.get('current_location')  is None:
            location_name = ""
        else:
            location_name = reverse_geocode(session.get('current_location').get('latitude'), session.get('current_location').get('longitude'))
            session['location_name']=location_name
        return render_template('profile_driver.html',user_name=user_name,current_location=location_name)



    
    return render_template('profile_driver.html')


@bp.route('/profile/driver/select_destination',methods=['GET','POST'])
@login_required
def driver_select_destination():
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
        destination=request.form.get('destination')
        session['destination']=destination
        return redirect('/profile/driver')       
    
    return render_template('driver_select_destination.html')

@bp.route('/profile/edit',methods=['GET','POST']) 
def edit_profile():
    return render_template('profile_edit.html')

