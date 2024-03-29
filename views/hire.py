from flask import Blueprint,render_template ,redirect,session
from flask_login import login_required,current_user
from models.vehicle import Vehicle 
from flask import url_for
from flask import request
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from logic.restrictions import *
from logic.matching import *
from models.booking import Booking
from kafka import KafkaProducer
import json





producer = KafkaProducer(bootstrap_servers='localhost:9092')

bp=Blueprint('hire',__name__)


@bp.route('/hire' ,methods=['GET','POST'])
@login_required
def hire():
    
    return render_template('hire.html')

@bp.route('/hire/car' ,methods=['GET','POST'])
@login_required
def hire_car():
    vehicle=Vehicle.query.filter_by(for_hire=True).all()
    listed_cars=[]
    for car in vehicle:
        if car.vehicle_type=="taxi" or car.vehicle_type=="hybrid":
            if car.for_hire==True:
                
                
            
                listed_cars.append(car)
    if len(listed_cars)==0:
        listed_cars=None

    user_name=current_user.user_name
    phone_number=current_user.phone
    date=datetime.now().strftime("%Y-%m-%d")
    time=datetime.now().strftime("%H:%M:%S")
    


    
    session['vehicle_type']='hire_car'
    if request.method=="POST":
        pickup_point='Contact to determine'
        destination='Contact to determine'
        vehicle_no=request.form.get('no_plate')
        vehicle=Vehicle.query.filter_by(no_plate=vehicle_no).first()
        
        booking=Booking(user_name, phone_number, date, time, pickup_point, destination, vehicle_no, booking_type='hire_car')
        booking.save()
        booking_notification={'vehicle':vehicle_no,'destination':destination,'rider':user_name,'timestamp':time,'booking_id':booking.id,'seen':False,'booking_type':'hire','pickup_point':pickup_point}
        session['booking']=booking_notification
        notifications.append(booking_notification)
        message = json.dumps(booking_notification)
        producer.send('booking_notification', value=message.encode())
        print(vehicle_no,'vehicle in booking')
                

        return redirect(url_for('booking.wait_confirmation'))
            


   


    return render_template('hire_car.html',cars=listed_cars)

@bp.route('/hire/bus',methods=['GET','POST'])
@login_required
def hire_bus():
    vehicle=Vehicle.query.filter_by(for_hire=True).all()
    listed_cars=[]
    for car in vehicle:
        if car.vehicle_type=="bus":
            if car.for_hire==True:
            
                listed_cars.append(car)
    if len(listed_cars)==0:
        listed_cars=None

    user_name=current_user.user_name
    phone_number=current_user.phone
    date=datetime.now().strftime("%Y-%m-%d")
    time=datetime.now().strftime("%H:%M:%S")
    pickup_point='waiting'
    destination=session.get('destination')
    session['vehicle_type']='hire_bus'


    if request.method=="POST":
        token=request.form.get('token')
        try:
            validate_csrf(token)
        except ValidationError :
            error="Invalid CSRF token"
            return error,404
        vehicle_no=request.form.get('no_plate')
        vehicle=Vehicle.query.filter_by(no_plate=vehicle_no).first()
        
        booking=Booking(user_name, phone_number, date, time, pickup_point, destination, vehicle_no, booking_type='hire_bus')
        booking.save()
        booking_notification={'vehicle':vehicle_no,'destination':destination,'rider':user_name,'timestamp':time,'booking_id':booking.id,'seen':False}
        session['booking']=booking_notification
        notifications.append(booking_notification)
        message = json.dumps(booking_notification)
        producer.send('booking_notification', value=message.encode())
        print(vehicle_no,'vehicle in booking')

        return redirect(url_for('booking.wait_confirmation'))
    

    return render_template('hire_bus.html',cars=listed_cars)




@bp.route('/hire/confirm',methods=['GET','POST'])
@login_required
@is_driver
def confirm_booking():
        user_name=current_user.user_name
        
        vehicle=Vehicle.query.filter_by(driver_username=user_name).first()
        if vehicle is None:
             vehicle=Vehicle.query.filter_by(owner_username=user_name).first()
             if vehicle is None:
                 
                 return render_template('hire_notifications.html',status=False,details=None)
        if vehicle.for_hire :
            status=True
        
            details=[]
            detail=receive_notification(notifications,session.get('vehicle'))
            session['notifications']=detail
            bookings=Booking.query.filter_by(vehicle_plate=vehicle.no_plate).all()
            for booking in bookings:
                 if booking.booking_type=="hire_car" or booking.booking_type=="hire_bus":
                      
                      details.append(booking)
            if details is None or len(details)==0:
                 details=None
                 
        else:
             status=False
             details=None
        
        
        
        
        if request.method=='POST':
                print('in post for hiring')
                token = request.form.get('csrf_token')
                try:
                        validate_csrf(token)
                except ValidationError :
                        error="Invalid CSRF token"
                form_name=(request.form.get('form-name'))
                print(form_name,'form name in confirm booking')
                if form_name=='disable':
                        vehicle.disallow_hiring()
                        
                        return redirect(url_for('hire.confirm_booking'))
                elif form_name=='enable':
                        print('in enable')
                        vehicle.allow_hiring()
                        return redirect(url_for('hire.confirm_booking'))
                else:
                    form_id=request.form.get('id')
                    print(form_id,'id in confirm booking')
                    
                    id=int(form_id)
                    print(id,'id in confirm booking')
                    confirmation=request.form.get('confirmation')
                    booking=Booking.query.filter_by(id=id).first()
                    
                            
                    if confirmation=='yes':
                            print(booking.Status,'booking in confirmed')
                            booking.confirm()
                           
                            print(booking.Status,'check booking in confirmed')
                            

                    else:
                            print('booking in cancelled')
                            booking.cancel()
                            
                    
                                        
                            
                    return render_template('hire_notifications.html',status=status,details=details)
               

        return render_template('hire_notifications.html',details=details,status=status)

