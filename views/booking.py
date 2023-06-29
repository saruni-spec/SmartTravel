from flask import render_template,Blueprint,session,redirect,url_for
from datetime import datetime
from flask import request
from logic.matching import *
from logic.routing import *
from models.stages import Stages
from models.booking import Booking
from models.vehicle import Vehicle
from flask_login import current_user
from flask_googlemaps import   Map
from kafka import KafkaConsumer,KafkaProducer
from flask import jsonify
from extensions.celery import process_notifications
from extensions.tasks import start_routing

from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError


from models.kafka import *
from flask_login import login_required
from .profile import is_driver








consumer_bus = KafkaConsumer('bus_coordinates',group_id='my-group',bootstrap_servers=['localhost:9092'],consumer_timeout_ms=10000)
consumer_taxi=KafkaConsumer('taxi_coordinates',group_id='taxi',bootstrap_servers=['localhost:9092'],consumer_timeout_ms=10000 )
consumer_hybrid=KafkaConsumer('hybrid_coordinates',group_id='hybrid',bootstrap_servers=['localhost:9092'],consumer_timeout_ms=10000 )
producer = KafkaProducer(bootstrap_servers='localhost:9092')

from datetime import datetime

def get_direction(vehicle_data, destination):
    if vehicle_data is None:
        return None
    bus_group = []
    for bus in vehicle_data:
            print(bus,'bus in get distance')
            bus_id = bus['vehicle']
            distance_to_destination = calculate_distance(destination['latitude'], destination['longitude'], bus['latitude'], bus['longitude'])
            bus_timestamp = datetime.strptime(bus['timestamp'], "%H:%M:%S")
            for other_bus in vehicle_data:
                if bus_id == other_bus['vehicle'] and bus is not other_bus:
                    other_bus_timestamp = datetime.strptime(other_bus['timestamp'], "%H:%M:%S")
                    if bus_timestamp > other_bus_timestamp:
                        other_bus_distance = calculate_distance(destination['latitude'], destination['longitude'], other_bus['latitude'], other_bus['longitude'])
                        if distance_to_destination < other_bus_distance:
                            if bus not in bus_group:
                                bus_group.append(bus)
    return bus_group

def closest_stage(user_location):
        stages_data =create_stage_dict( Stages.query.all())
        stage_clusters=group_coordinates(stages_data, 5)
        
        print(user_location,'closest stage')
        latitude=float(user_location['latitude'])
        longitude=float(user_location['longitude'])
        print(latitude,longitude,'in closest stage')
        closest_stage=(find_closest_bus_stop(latitude, longitude, stage_clusters))
    
        destination_lat = float(closest_stage['latitude'])
        destination_lng = float(closest_stage['longitude'])
        distance = get_distance(latitude, longitude, destination_lat, destination_lng)

        return[closest_stage,distance]

def closest_taxi(user_location,taxi_data):
        taxi_clusters=group_coordinates(taxi_data, 5)
        print(user_location,'closest taxi')
        latitude=float(user_location['latitude'])
        longitude=float(user_location['longitude'])
        print(latitude,longitude,'in closes taxi')
        closest_taxi=(find_closest_bus_stop(latitude, longitude, taxi_clusters))
    
        if closest_taxi is None:
                return None
        else:
                destination_lat = float(closest_taxi['latitude'])
                destination_lng = float(closest_taxi['longitude'])
        distance = get_distance(latitude, longitude, destination_lat, destination_lng)
        return[closest_taxi,distance]



def bus(bus_data,stage,user_time,destination,closest_stage):
        
        bus_clusters=group_coordinates(bus_data, 5)
        print(bus_clusters,'closest bus')
        latitude = float(stage[0]['latitude']) 
        longitude = float(stage[0]['longitude'])
        print(latitude,longitude ,'in closest bus')
        closest_bus=(find_bus(bus_clusters,stage,user_time))
        if closest_bus is None:
                return None
        else:
                
                return closest_bus



bp=Blueprint('booking',__name__)

@bp.route('/booking/select_destination',methods=['GET','POST'])  
@login_required
def select_destination():
        
        user_location=session.get('current_location')
        user_location_name=session.get('location_name')
        if user_location is None:
                user_location=None
        print(user_location,'user location in post up')
        print(jsonify(user_location),'user location in jsonify up')
        if request.method=='POST':
                token = request.form.get('csrf_token')
                try:
                        validate_csrf(token)
                except ValidationError :
                        error="Invalid CSRF token"
                        return error,404
                form_name = request.form.get('form-name')
                print(form_name,'form name')
                if form_name == 'destination-form':
                        bus_data=create_kafka_objects(consumer_bus)
                        print(bus_data,'bus data fro kafka')
                        taxi_data=create_kafka_objects(consumer_taxi)
                        print(taxi_data,'taxi data from kafka')
                        
                        destination_name=request.form.get('destination')
                        print(destination_name,'destination selected in form')
                        if destination_name=='':
                                error='Please select Destination'
                                return render_template('booking_select_destination.html',user_location=user_location,error=error)
                        session['destination']=destination_name
                        import requests

                        api_key = "AIzaSyA_JxBRmUKjcpPLWXwAagTX9k19tIWi2SQ"

                        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={destination_name}&key={api_key}"
                        response = requests.get(url)
                        data = response.json()
                        if data['status'] == 'OK':
                                result = data['results'][0]
                                location = result['geometry']['location']
                                latitude = location['lat']
                                longitude = location['lng']
                                destination={'location':destination_name,'latitude':latitude,'longitude':longitude,'user':current_user.user_name}
                                print(destination['location'],'destination after geocoding')
                        else:
                                error= "Unable to retrieve coordinates."
                        session['destination_coordinates']={'latitude':destination['latitude'],'longitude':destination['longitude']}
                        
                        same_direction_buses=get_direction(bus_data,destination)
                        
                        print(same_direction_buses,'same direction buses')
                        nearest_stage=closest_stage(user_location)
                        print(nearest_stage[0]['stage_name'],'nearest stage to user')
                        if user_location is None or user_location=='':
                                error='Please select your location'
                                return render_template('booking_select_destination.html',error=error)
                        nearest_taxi=closest_taxi(user_location,taxi_data)
                        print(nearest_taxi,'nearest taxi in post')
                        if nearest_taxi is None:
                                my_taxi=None
                                taxi_message='No taxi nearby'
                        else:
                                print('we have a nearest taxi')
                                taxi_location_name=reverse_geocode(nearest_taxi[0]['latitude'], nearest_taxi[0]['longitude'])
                                session['taxi_location_name']=taxi_location_name
                                taxi_arrival_time=get_time(user_location_name, taxi_location_name,"driving", api_key)
                                session['arrival_time']=taxi_arrival_time
                                my_taxi=nearest_taxi[0]['vehicle']
                                taxi_message='Click here to book your taxi'
                                taxi_time=get_time(session.get('location_name'), destination_name,"driving", api_key)
                                print(taxi_time,'taxi time in post')
                                session['taxi_travel_time']=get_time(destination_name,session.get('location'),'driving',api_key)
                                print (session.get('taxi_travel_time'),'taxi travel time ')
                        
                        
                        
                        user_time=get_time(session.get('location_name'), nearest_stage[0]['stage_name'],"walking", api_key)
                        print(f"{user_time} Time needed for user to walk to stage {nearest_stage[0]['stage_name']}")
                        bus_time=get_time(nearest_stage[0]['stage_name'], destination_name,"driving", api_key)
                        print(f"{bus_time} Total time for user to get to destination on bus")
                        a_bus=bus(same_direction_buses,nearest_stage,user_time)
                        if a_bus is None:
                                bus_message='No bus nearby'
                                

                        else:
                                
                                #bus_location_name=reverse_geocode(a_bus[0]['latitude'], a_bus[0]['longitude'])
                                #bus_arrival_time=get_time(nearest_stage[0]['stage_name'], bus_location_name,"driving", api_key)
                                #my_bus=a_bus[0]['vehicle']
                                for each_bus in a_bus:
                                        bus_location=reverse_geocode(each_bus['latitude'], each_bus['longitude'])
                                        bus['arrival_time']=get_time(nearest_stage[0]['stage_name'],bus_location,'driving',api_key)
                                bus_message='Click here to select a bus'
                                session['user_to_stage_time']=user_time
                                session['bus_travel_time']=get_time(nearest_stage[0]['stage_name'],destination_name,'driving',api_key)
                        print(a_bus,'a bus in post')
                        session['closest_bus']=a_bus
                        session['closest_taxi']=my_taxi
                        session['closest_stage']=nearest_stage[0]['stage_name']
                        session['pickup_point']=user_location_name
                
                        return render_template('booking_select_destination.html',closest_bus=bus_message,closest_taxi=taxi_message,user_location=user_location_name)
                elif form_name == 'taxi-form':
                        
                        session['vehicle_type']='taxi'
                        
                        return redirect(url_for('booking.select_taxi'))
                elif form_name == 'bus-form':
                        
                        session['vehicle_type']='bus'
                        
                        return redirect(url_for('booking.bus_options'))
                elif form_name == 'hybrid-form':
                        pass
        return render_template('booking_select_destination.html',user_location=user_location_name)



notifications=[]

@bp.route('/booking/select_taxi',methods=['GET','POST'])
@login_required
def select_taxi():
        user_name=current_user.user_name
        print(user_name,'user name in select taxi')
        phone_number=current_user.phone
        date=datetime.now().strftime("%Y-%m-%d")
        time=datetime.now().strftime("%H:%M:%S")
        destination=session.get('destination')
        vehicle_no=session.get('closest_taxi')
        print(vehicle_no,'vehicle no in select vehicle')
        vehicle_type=session.get('vehicle_type')
        travel_time=session.get('taxi_travel_time')
        
        pickup_point=session.get('pickup_point')
        arrival_time=session.get('arrival_time')
       
        vehicle=Vehicle.query.filter_by(no_plate=vehicle_no).first()
        
        fare=10
        
        if request.method=='POST':
                booking=Booking(user_name, phone_number, date, time, pickup_point, destination, vehicle_no, fare)
                booking.save()
                booking_notification={'vehicle':vehicle_no,'destination':destination,'pickup_point':pickup_point,'rider':user_name,'timestamp':time,'booking_id':booking.id}
                session['booking']=booking_notification
                notifications.append(booking_notification)
                message = json.dumps(booking_notification)
                producer.send('booking_notification', value=message.encode())
                print(vehicle_no,'vehicle in booking')
                

                return redirect(url_for('booking.wait_confirmation'))
        

                



        return render_template('booking_select_taxi.html',travel_time=travel_time,fare=fare,vehicle_no=vehicle_no,arrival_time=arrival_time,pickup_point=pickup_point,destination=destination,vehicle_type=vehicle_type)


@bp.route('/booking/bus_options',methods=['GET','POST'])
@login_required
def bus_options():
        buses=session.get('closest_bus')
        pickup_point=session.get('closest_stage')
        travel_time=session.get('travel time')
        
        user_name=current_user.user_name
        print(user_name,'user name in select taxi')
        phone_number=current_user.phone
        date=datetime.now().strftime("%Y-%m-%d")
        time=datetime.now().strftime("%H:%M:%S")
        destination=session.get('destination')
        
        fare=10
        print(pickup_point,'pickup point in bus options')
        print(buses,'buses in bus options')
        if request.method=='POST':
                vehicle_no=request.form.get('vehicle')
                booking=Booking(user_name, phone_number, date, time, pickup_point, destination, vehicle_no, fare)
                booking.save()
                booking_notification={'vehicle':vehicle_no,'destination':destination,'pickup_point':pickup_point,'rider':user_name,'timestamp':time,'booking_id':booking.id}
                session['booking']=booking_notification
                notifications.append(booking_notification)
                message = json.dumps(booking_notification)
                producer.send('booking_notification', value=message.encode())
                print(vehicle_no,'vehicle in booking')
                
                return redirect(url_for('booking.wait_confirmation'))

        return render_template('booking_bus_options.html',buses=buses,pickup_point=pickup_point,destination=destination,travel_time=travel_time)


from datetime import datetime, timedelta
def receive_notification(notifications ,current_vehicle):
        current_notifiations=[]
        current_time = datetime.now()
        for notification in notifications:
            if notification['vehicle']==current_vehicle:
                timestamp = datetime.strptime(notification['timestamp'], "%H:%M:%S")
                time_difference = current_time - timestamp
                if time_difference > timedelta(minutes=3):
                    print(notification,'sent to driver')
                    current_notifiations.append(notification)
            
                
        return current_notifiations 








@bp.route('/booking/confirm',methods=['GET','POST'])
@login_required
@is_driver
def confirm_booking():
        booking_notification=session.get('booking')
        details=[]
        details=receive_notification(notifications,session.get('vehicle'))
        
        confirmed_message='waiting'


        if request.method=='POST':
                token = request.form.get('csrf_token')
                try:
                        validate_csrf(token)
                except ValidationError :
                        error="Invalid CSRF token"

                id=request.form.get('id')
                
                

                confirmation=request.form.get('confirmation')
                booking=Booking.query.filter_by(id=id).first()
                
                        
                if confirmation=='yes':
                        print(booking.Status,'booking in confirmed')
                        booking.confirm()
                        confirmed_message='Booking confirmed'
                        print(booking.Status,'check booking in confirmed')
                        return render_template('booking_confirm.html',details=details,confirmed_message=confirmed_message)

                else:
                        print('booking in cancelled')
                        booking.cancel()
                        confirmed_message='Booking cancelled'
                for notification in details:
                        if notification['booking_id']==id:
                                notification['status']='Cancelled'
                        else:
                               notification['status']='Confirmed'
                return render_template('booking_confirm.html',details=details,confirmed_message=confirmed_message)
               

        return render_template('booking_confirm.html',details=details,confirmed_message=confirmed_message,booking_notification=booking_notification)



@bp.route('/booking/wait_confirmation',methods=['GET','POST'])
@login_required
def wait_confirmation():
       waiting_message='Your booking is in process. Please wait for confirmation.'
       booking_notification=session.get('booking')
       vehicle_no=session.get('booking')['vehicle']
       destination=session.get('booking')['destination']
       pickup_point=session.get('booking')['pickup_point']
       booking_id=session.get('booking')['booking_id']
       booking=Booking.query.filter_by(id=booking_id).first()
       if request.method=='POST':
        token = request.form.get('csrf_token')
        try:
                validate_csrf(token)
        except ValidationError :
                error="Invalid CSRF token"
        confirm=request.form.get('confirm')
        
        
        if confirm=='check':
                while 1:
                        booking=Booking.query.filter_by(id=booking_id).first()
                        print(booking.Status,'booking in check here')
                        if booking.Status=='confirmed':
                                        waiting_message='Booking confirmed'
                                        break
                        elif booking.Status=='Cancelled':
                                        waiting_message='Booking cancelled'
                                        break
                                
        
                if waiting_message=='Booking confirmed':
                        return redirect(url_for('booking.wait_for_vehicle'))
                else:
                        return redirect(url_for('booking.select_vehicle'))
                                
               
        
                      
       return render_template('booking_wait_confirmation.html',booking_notification=booking_notification,waiting_message=waiting_message,vehicle_no=vehicle_no,destination=destination,pickup_point=pickup_point)




@bp.route('/booking/wait_for_vehicle',methods=['GET','POST'])
@login_required
def wait_for_vehicle():
    user_name=current_user.user_name
    vehicle_no=session.get('booking')['vehicle']
    destination=session.get('booking')['destination']
    pickup_point=session.get('booking')['pickup_point']
    wait_time=session.get('arrival_time')
    
    
    start_routing.delay()
    return render_template('booking_wait_for_vehicle.html',user_name=user_name,wait_time=wait_time,vehicle_no=vehicle_no,destination=destination,pickup_point=pickup_point)



           


@bp.route('/booking/review',methods=['GET','POST'])
@login_required
@is_driver
def review():
        return render_template('booking_review.html')