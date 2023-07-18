from flask import render_template, Blueprint, request, session,redirect,url_for
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required,current_user
from logic.routing import *
from kafka import KafkaProducer,KafkaConsumer
import json

from models.user import User

from extensions.extensions import db
from logic.restrictions import *
from logic.validation import valid_number,valid_licence




producer = KafkaProducer(bootstrap_servers='localhost:9092')

bp = Blueprint('profile', __name__) 

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
    if current_user.check_if_driver() and current_user.check_if_owner():
        print('driver and owner')
        return redirect(url_for('profile.profile_driver'))
    elif current_user.check_if_owner() and not current_user.check_if_driver():
        print('owner and not driver')
        
        return redirect(url_for('profile.profile_owner'))
    elif current_user.check_if_driver() and not current_user.check_if_owner():
        print('driver and not owner')
        
        return redirect(url_for('profile.profile_driver'))

    elif not current_user.check_if_driver() and not current_user.check_if_owner():
        print('not driver and not owner')
        
        
        return redirect(url_for('profile.rider'))
    




@bp.route('/profile/rider', methods=['GET', 'POST'])
@login_required
def rider():
    user_name=current_user.user_name
    user=User.query.filter_by(user_name=user_name).first()
    email=user.email
    phone_number=user.phone
    address=user.address
    first_name=user.first_name
    other_name=user.other_name
    card=user.card_number
    
   
    return render_template('profile_rider.html',first_name=first_name,other_name=other_name,card=card,user_name=user_name,email=email,phone_number=phone_number,address=address)
            

@bp.route('/profile/owner', methods=['GET', 'POST'])
@login_required
@is_owner
def profile_owner():
    user_name=current_user.user_name
    user=User.query.filter_by(user_name=user_name).first()
    email=user.email
    phone_number=user.phone
    address=user.address
    first_name=user.first_name
    other_name=user.other_name
    card=user.card_number
    vehicles=Vehicle.query.filter_by(owner_username=user_name).first()
    vehicle_no=vehicles.no_plate


   
    

    return render_template('profile_owner.html',vehicle_no=vehicle_no,first_name=first_name,other_name=other_name,card=card,user_name=user_name,email=email,phone_number=phone_number,address=address)


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
    print(docked,'docked in profile nnnn')
    user_name=current_user.user_name
    vehicle=Vehicle.query.filter_by(driver_username=user_name).first()
    user=User.query.filter_by(user_name=user_name).first()
    email=user.email
    phone_number=user.phone
    address=user.address
    first_name=user.first_name
    other_name=user.other_name
    
    vehicle_no=vehicle.no_plate
    
    session['my_vehicle']=vehicle.no_plate
    stages=Stages.query.all()
    fare=vehicle.fare
    
    if request.method == 'POST':
        token = request.form.get('csrf_token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
            return error,404
        
        

        is_docked=request.form.get('is_docked')
        print(is_docked,'is_docked in profile')
        if is_docked == 'on':
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
                return render_template('profile_driver.html',error=error,fare=fare,vehicle_no=vehicle_no,docked=docked,first_name=first_name,other_name=other_name,user_name=user_name,email=email,phone_number=phone_number,address=address)
        else:
            session['is_docked'] = False
            session['docked']=False
            
            
    return render_template('profile_driver.html',fare=fare,vehicle_no=vehicle_no,docked=docked,first_name=first_name,other_name=other_name,user_name=user_name,email=email,phone_number=phone_number,address=address)


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
        error=None
        
        form_name=request.form.get('form-name')
        if form_name=='delete':
            print ('delete')
            return redirect(url_for('profile.delete_profile'))

        else:
            print('not delete')
            user_name=request.form.get('user_name')
            if user_name !='':
                print('user_name here')
                if current_user.user_name!=user_name:
                    print('changing username')
                    user_check=User.query.filter_by(user_name=user_name).first()
                    if user_check is None:
                        user.change_user_name(user_name)
                    else:
                        error='Username already taken'
            email=request.form.get('email')
            if email !='':
                print('email here')
                
                if user.email!=email:
                    print('changing email')
                    
                    error=validate_email(email)
                    if not error:
                        user.add_email(email)

            phone_number=request.form.get('phone')
            if phone_number !='':
                print('phone_number here')
                print(user.phone)
                print(phone_number)
                if user.phone != phone_number:
                    print('changing phone')

                    valid=valid_number(phone_number)
                    if valid:    
                        user.add_phone(phone_number)
                    else:
                        error='Invalid phone number'

            
            address=request.form.get('address')
            if address !='':
                print('address here')
                if user.address!=address:
                    print('changing address')
                    user.add_address(address)
            
            card_number=request.form.get('card')
            if card_number !='':
                print('card_number here')
                if user.card_number!=card_number:
                    print('changing card')
                    valid=valid_licence(card_number)
                    if valid:
                        user.add_card_number(card_number)
                    else:
                        error='Invalid card number(10 digits)'

            if error is None:
                db.session.commit()
                return redirect(url_for('profile.profile'))
            else:
                return render_template('profile_edit.html',error=error,user_name=user_name,email=email,phone=phone_number,address=address,card=card_number)
    return render_template('profile_edit.html',user_name=current_user.user_name,email=user.email,phone=user.phone,address=user.address,card=user.card_number)



@bp.route('/profile/vehicle',methods=['GET','POST'])
@login_required
def vehicle():
    user_name=current_user.user_name
    user=User.query.filter_by(user_name=user_name).first()
    vehicle=Vehicle.query.filter_by(driver_username=user_name).first()
    if vehicle is None:
        vehicle=Vehicle.query.filter_by(owner_username=user_name).first()
    color=vehicle.color
    no_plate=vehicle.no_plate
    capacity=vehicle.capacity
    model=vehicle.build_type
    service_type=vehicle.vehicle_type
    for_hire=vehicle.for_hire
    fare=vehicle.fare
    hire_cost=vehicle.hiring_cost
    driver_name=vehicle.driver_username
    owner_name=vehicle.owner_username
    return render_template('profile_vehicle.html',driver_name=driver_name,owner_name=owner_name,hire_cost=hire_cost,fare=fare,color=color,no_plate=no_plate,capacity=capacity,model=model,service_type=service_type,for_hire=for_hire)


@bp.route('/profile/vehicle/edit',methods=['GET','POST'])
@login_required
def vehicle_edit():
    user_name=current_user.user_name
    vehicle=Vehicle.query.filter_by(owner_username=user_name).first()
    color=vehicle.color
    capacity=vehicle.capacity
    service_type=vehicle.vehicle_type
    fare=vehicle.fare
    hire_cost=vehicle.hiring_cost
    if request.method == 'POST':
        color=request.form.get('color')
        capacity=request.form.get('capacity')
        service_type=request.form.get('service_type')
        fare=request.form.get('fare')
        hire_cost=request.form.get('hire_cost')
        if color !='':
            vehicle.change_color(color)
        if capacity !='':
            vehicle.change_capacity(capacity)
        if service_type !='':
            vehicle.change_type(service_type)
        if fare !='':
            vehicle.set_fare(fare)
        if hire_cost !='':
            vehicle.set_hiring_cost(hire_cost)
        
        
        
        return redirect(url_for('profile.vehicle'))
    return render_template('profile_vehicle_edit.html',fare=fare,hire_cost=hire_cost,color=color,capacity=capacity,service_type=service_type)

from flask_login import logout_user
@bp.route('/profile/delete',methods=['GET','POST'])
@login_required
def delete_profile():
    user_name=current_user.user_name
    user=User.query.filter_by(user_name=user_name).first()
    if user.check_if_owner() and not user.check_if_driver():
        vehicle=Vehicle.query.filter_by(owner_username=user_name).first()
        other_driver=vehicle.driver_username
        other_driver_user=Driver.query.filter_by(user_name=other_driver).first()
        driver_user=User.query.filter_by(user_name=other_driver).first()
        
        owner=Owner.query.filter_by(user_name=user_name).first()
        status='level4'
        message='As an owner. Deleting this profile will delete your vehicle,suspend its driver and change your status to rider'
    elif user.check_if_driver() and user.check_if_owner():
        vehicle=Vehicle.query.filter_by(driver_username=user_name).first()
        driver=Driver.query.filter_by(user_name=user_name).first()
        owner=Owner.query.filter_by(user_name=user_name).first()
        status='level3'
        message=' Deleting this profile will delete your vehicle and change your status to rider'
    elif user.check_if_driver() and not user.check_if_owner():
        driver=Driver.query.filter_by(user_name=user_name).first()
        status='level2'
        message=' Deleting this profile will change your status to rider'
    else:
        status='level1'
        
        message=' Deleting this profile will delete your profile'
    
    if request.method == 'POST':
        if status=='level1':
            

            user.delete()
            logout_user()
        elif status=='level2':
            
            
            driver.delete()
            user.make_user()
            logout_user()
        elif status=='level3':
            
            
            vehicle.delete()
            
            driver.delete()
            
            owner.delete()
            user.make_user()
            logout_user()
        elif status=='level4':
            vehicle.delete()
            
            other_driver_user.delete()
            
            driver_user.role='user'
            
            
            
            
            owner.delete()
            user.make_user()
            logout_user()
        return redirect(url_for('login.logout'))
        
            
            
    return render_template('profile_delete.html',message=message)