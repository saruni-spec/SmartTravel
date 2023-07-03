from flask import render_template, Blueprint, request, session,redirect,url_for
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required,current_user
from logic.routing import *
from kafka import KafkaProducer,KafkaConsumer
import json
from functools import wraps
from models.owner import Owner
from models.driver import Driver
from models.user import User

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

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        if current_user.check_if_driver():
            return redirect(url_for('profile.profile_driver'))
        elif current_user.check_if_owner:
            return redirect(url_for('profile.profile_owner'))
        else:
            return redirect(url_for('profile.rider'))
    else:
        return redirect(url_for('login.login'))




@bp.route('/profile/rider', methods=['GET', 'POST'])
@login_required
def rider():
    user_name=current_user.user_name
   
    return render_template('profile_rider.html',user_name=user_name)
            

@bp.route('/profile/owner', methods=['GET', 'POST'])
@login_required
@is_owner
def profile_owner():
    user_name=current_user.user_name
    

    return render_template('profile_owner.html',user_name=user_name)


from models.kafka import create_kafka_notifications,remove_duplicate_notifications
from models.vehicle import Vehicle
from models.stages import Stages
from logic.matching import find_closest_bus_stop_to_bus
from datetime import datetime

@bp.route('/profile/driver', methods=['GET', 'POST'])
@login_required
@is_driver
def profile_driver():
    from extensions.tasks import start_booking
    docked = session.get('docked', False)
    user_name=current_user.user_name
    vehicle=Vehicle.query.filter_by(driver_username=user_name).first()
    capacity=vehicle.capacity
    session['my_vehicle']=vehicle.no_plate
    stages=Stages.query.all()
    
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
            return error,404
        
        

        
        print(vehicle.capacity,'capacity in profile')
        error=None
        destination= request.form.get('destination')
        start_booking.delay()
        coordinates=session.get('tracking_coordinates')
        if coordinates is not None:
            docking_stage=find_closest_bus_stop_to_bus(coordinates['latitude'],coordinates['longitude'],stages)
            session['docking_stage']=docking_stage.stage_name
        else:
            error="Please turn on GPS"
        session['is_docked'] = True
        session['bus_destination'] = destination
        print(destination,'destination in proifle')
        session['docked']=True
        if error:
            return render_template('profile_driver.html',user_name=user_name,capacity=capacity,error=error,docked=docked)
        
    return render_template('profile_driver.html',user_name=user_name,capacity=capacity,docked=docked)


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
    from logic.validation import validate_email,validate_password
    username=current_user.user_name
    user=User.query.filter_by(user_name=username).first()
    if request.method == 'POST':

        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
        
        

        user_name=request.form.get('user_name')
        if user_name !='':
            if current_user.user_name!=user_name:
                user.change_user_name(user_name)
        email=request.form.get('email')
        if email !='':
            if current_user.email!=email:
                error=validate_email(email)
                if not error:
                    user.add_email(email)

        phone_number=request.form.get('phone_number')
        if phone_number !='':
            if current_user.phone!=phone_number:
                user.add_phone(phone_number)
        

        
        address=request.form.get('address')
        if address !='':
            if current_user.address!=address:
                user.add_address(address)
        
        
        if error is None:
            db.session.commit()
            return redirect(url_for('profile.profile_driver'))
        else:
            return render_template('profile_edit.html',error=error)
    return render_template('profile_edit.html',user_name=current_user.user_name,email=current_user.email,phone=current_user.phone,address=current_user.address)




