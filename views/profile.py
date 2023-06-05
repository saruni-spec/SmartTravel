from flask import render_template, Blueprint, request, session
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required
from logic.routing import *
from kafka import KafkaProducer
import json





producer = KafkaProducer(bootstrap_servers='localhost:9092')
bp = Blueprint('profile', __name__) 


@bp.route('/profile/rider', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        session['current_location'] = {"latitude": latitude, "longitude": longitude}
        message = json.dumps({"latitude": latitude, "longitude": longitude})
        producer.send('user_coordinates', value=message.encode())
        location_name = reverse_geocode(latitude, longitude)
        print(location_name,':',latitude, 'latitude',longitude, 'longitude')
        user_name=session.get('user_name')
        print(session.get('current_location'),'current_location')

        return render_template('profile_rider.html',user_name=user_name)



    
    return render_template('profile_rider.html')
            

@bp.route('/profile/driver', methods=['GET', 'POST'])
@login_required
def profile_driver():
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        session['current_location'] = {"latitude": latitude, "longitude": longitude}
        message = json.dumps({"latitude": latitude, "longitude": longitude})
        producer.send('user_coordinates', value=message.encode())
        location_name = reverse_geocode(latitude, longitude)
        print(location_name,':',latitude, 'latitude',longitude, 'longitude')

        return render_template('profile_driver.html')



    
    return render_template('rider_profile.html')

@bp.route('/profile/owner', methods=['GET', 'POST'])
@login_required
def profile_owner():
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        session['current_loation'] = {"latitude": latitude, "longitude": longitude}
        message = json.dumps({"latitude": latitude, "longitude": longitude})
        producer.send('user_coordinates', value=message.encode())
        
        
        location_name = reverse_geocode(latitude, longitude)
        print(location_name,':',latitude, 'latitude',longitude, 'longitude')

        return render_template('profile_owner.html')



    
    return render_template('rider_profile.html')
@bp.route('/profile/edit',methods=['GET','POST']) 
def edit_profile():
    return render_template('profile_edit.html')

