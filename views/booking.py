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
from logic.restrictions import *







consumer_notifications=KafkaConsumer('booking_notification',group_id='notifications',bootstrap_servers=['localhost:9092'],consumer_timeout_ms=10000)
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



def bus(bus_data):
        if bus_data is None or len(bus_data)==0:
                return None
        
        bus_clusters=group_coordinates(bus_data, 5)
        print(bus_clusters,'closest bus')
        if bus_clusters is None:
                return None
        buses=[]
        for cluster_label, bus_list in bus_clusters.items():
               for bus in bus_list:
                       buses.append(bus)
               
        return buses


bp=Blueprint('booking',__name__)

@bp.route('/booking/select_destination',methods=['GET','POST'])  
@login_required
def select_destination():
        
        user_location=session.get('current_location',None)
        user_location_name=session.get('location_name')
        destination_name=session.get('destination',None)

        print(user_location,'user location in post up')
        
        taxi_message=session.get('taxi_message',None)
        hybrid_message=session.get('hybrid_message',None)
        bus_message=session.get('bus_message',None)
        
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
                        old_bus_data=data = [
    {
        "vehicle": "EFG901",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-06-30 21:30:00",
        "bus_destination": "Nairobi CBD",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "HIJ234",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-06-30 22:45:00",
        "bus_destination": "Ruiru",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "KLM567",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-06-30 23:59:00",
        "bus_destination": "Ruiru",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "NOP890",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-07-01 01:15:00",
        "bus_destination": "Juja ",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "QRS123",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-07-01 02:30:00",
        "bus_destination": "Thika",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "ABC123",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-06-30 09:00:00",
        "bus_destination": "Juja",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "DEF456",
        "latitude": -1.23488,
        "longitude": 36.8892,
        "timestamp": "2023-06-30 10:15:00",
        "bus_destination": "Juja",
        "docked": True,
        "docking_stage": "Ruaraka (Getrude's Children's Hospital)"
    },
    {
        "vehicle": "GHI789",
        "latitude": -1.18699,
        "longitude": 36.9199,
        "timestamp": "2023-06-30 11:30:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kahawa West"
    },
    {
        "vehicle": "JKL012",
        "latitude": -1.21418,
        "longitude": 36.8907,
        "timestamp": "2023-06-30 12:45:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Roysambu"
    },
    {
        "vehicle": "MNO345",
        "latitude": -1.09793,
        "longitude": 37.0166,
        "timestamp": "2023-06-30 14:00:00",
        "docked": False,
        
    },
    {
        "vehicle": "PQR678",
        "latitude": -1.17554,
        "longitude": 36.9411,
        "timestamp": "2023-06-30 15:15:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kahawa Sukari"
    },
    {
        "vehicle": "STU901",
        "latitude": -1.22054,
        "longitude": 36.9029,
        "timestamp": "2023-06-30 16:30:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kasarani Sports Complex"
    },
    {
        "vehicle": "VWX234",
        "latitude": -1.14406,
        "longitude": 36.9608,
        "timestamp": "2023-06-30 17:45:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kenyatta University"
    },
    {
        "vehicle": "YZA567",
        "latitude": -1.18345,
        "longitude": 36.9272,
        "timestamp": "2023-06-30 19:00:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kahawa Wendani"
    },
    {
        "vehicle": "BCD890",
        "latitude": -1.03867,
        "longitude": 37.0768,
        "timestamp": "2023-06-30 20:15:00",
        "docked": False,
        
    }
]

                        print(old_bus_data,'bus data fro kafka')
                        bus_data = [bus for bus in old_bus_data if bus['docked']]
                        taxi_data=create_kafka_objects(consumer_taxi)
                        print(taxi_data,'taxi data from kafka')
                        hybrid_data=create_kafka_objects(consumer_hybrid)
                        print(hybrid_data,'hybrid data from kafka')
                        
                        destination_name=request.form.get('destination')
                        print(destination_name,'destination selected in form')
                        if destination_name=='':
                                error='Please select Destination'
                                return render_template('booking_select_destination.html',user_location=user_location,user_location_name=user_location_name,error=error)
                        session['destination']=destination_name
                        destination=geocode(api_key,destination_name,current_user)
                        if destination is None:
                                error='Check your Internet COnnection'
                                return render_template('booking_select_destination.html',error=error,user_location=user_location,user_location_name=user_location_name)
                                
                        session['destination_coordinates']={'latitude':destination['latitude'],'longitude':destination['longitude']}
                        
                        
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
                                session['taxi_location']={'latitude':nearest_taxi[0]['latitude'],'longitude':nearest_taxi[0]['longitude']}
                                session['taxi_location_name']=taxi_location_name
                                taxi_arrival_time=get_time(user_location_name, taxi_location_name,"driving", api_key)
                                session['taxi_arrival_time']=taxi_arrival_time
                                my_taxi=nearest_taxi[0]['vehicle']
                                taxi_message='Click here to book your taxi'
                                taxi_time=get_time(session.get('location_name'), destination_name,"driving", api_key)
                                print(taxi_time,'taxi time in post')
                                session['taxi_travel_time']=get_time(destination_name,session.get('location_name'),'driving',api_key)
                                print (session.get('taxi_travel_time'),'taxi travel time ')
                        
                        
                        
                        user_time=get_time(session.get('location_name'), nearest_stage[0]['stage_name'],"walking", api_key)
                        print(f"{user_time} Time needed for user to walk to stage {nearest_stage[0]['stage_name']}")
                        bus_time=get_time(nearest_stage[0]['stage_name'], destination_name,"driving", api_key)
                        print(f"{bus_time} Total time for user to get to destination on bus")
                        session['travel_time']=bus_time

                        routed_bus_data=find_route(bus_data)
                        viable_buses=allow_passenger(routed_bus_data,destination_name,nearest_stage[0]['stage_name'])

                        a_bus=bus(viable_buses)
                        if a_bus is None:
                                bus_message='No bus nearby'
                                

                        else:
                                
                                #bus_location_name=reverse_geocode(a_bus[0]['latitude'], a_bus[0]['longitude'])
                                #bus_arrival_time=get_time(nearest_stage[0]['stage_name'], bus_location_name,"driving", api_key)
                                #my_bus=a_bus[0]['vehicle']
                                
                                bus_message='Click here to select a bus'
                                session['user_to_stage_time']=user_time
                                session['bus_travel_time']=get_time(nearest_stage[0]['stage_name'],destination_name,'driving',api_key)
                        print(a_bus,'a bus in post')
                        session['bus_location']={'latitude':nearest_stage[0]['latitude'],'longitude':nearest_stage[0]['longitude']}
                        session['closest_bus']=a_bus
                        session['closest_taxi']=my_taxi
                        session['closest_stage']=nearest_stage[0]['stage_name']
                        session['taxi_pickup_point']=user_location_name
                        session['taxi_message']=taxi_message
                        session['bus_message']=bus_message

                        nearest_hybrid_to_user=closest_taxi(user_location,hybrid_data)
                        print(nearest_hybrid_to_user,'nearest hybrid to user')
                        
                        if nearest_hybrid_to_user is None:
                                nearest_hybrid_to_stage=find_closest_hybrid_to_stage(nearest_stage[0]['latitude'],nearest_stage[0]['longitude'],hybrid_data)
                                my_hybrid=nearest_hybrid_to_stage
                                print(nearest_hybrid_to_stage,'nearest hybrid to stage')
                                if my_hybrid is None or len(my_hybrid)==0:
                                        print('no hybrid nearby')
                                        hybrid_message='No hybrid nearby'
                                        session['closest_hybrid']=None
                                        
                                else:
                                        
                                        hybrid_location_name=reverse_geocode(my_hybrid[0]['latitude'], my_hybrid[0]['longitude'])
                                        session['hybrid_location_name']=hybrid_location_name
                                        hybrid_arrival_time=get_time(nearest_stage[0]['stage_name'], hybrid_location_name,"driving", api_key)
                                        hybrid_time=get_time(nearest_stage[0]['stage_name'], destination_name,"driving", api_key)
                                        session['hybrid_pickup_point']=nearest_stage[0]['stage_name']
                                        my_hybrid_now=my_hybrid[0]['vehicle']
                                        hybrid_message='Click here to book your ride'
                                        session['hybrid_arrival_time']=hybrid_arrival_time
                                        session['hybrid_travel_time']=hybrid_time
                                        session['closest_hybrid']=my_hybrid_now
                        else:
        
                                my_hybrid=nearest_hybrid_to_user
                                hybrid_location_name=reverse_geocode(my_hybrid[0]['latitude'], my_hybrid[0]['longitude'])
                                session['hybrid_location_name']=hybrid_location_name
                                hybrid_arrival_time=get_time(user_location_name, hybrid_location_name,"driving", api_key)
                                hybrid_time=get_time(session.get('location_name'), destination_name,"driving", api_key)
                                session['hybrid_pickup_point']=user_location_name
                                session['hybrid_arrival_time']=hybrid_arrival_time
                                my_hybrid_now=my_hybrid[0]['vehicle']
                                session['hybrid_travel_time']=hybrid_time
                        
                                hybrid_message='Click here to book your ride'
                                

                                session['closest_hybrid']=my_hybrid_now
                        session['hybrid_location']={'latitude':my_hybrid[0]['latitude'],'longitude': my_hybrid[0]['longitude']}
                        session['hybrid_message']=hybrid_message
                        return render_template('booking_select_destination.html',closest_bus=bus_message,closest_taxi=taxi_message,user_location=user_location,user_location_name=user_location_name,closest_hybrid=hybrid_message,destination=destination_name)
                elif form_name == 'taxi-form':
                        if session.get('closest_taxi') is None:
                                return render_template('booking_select_destination.html',closest_bus=bus_message,closest_taxi=taxi_message,user_location=user_location,user_location_name=user_location_name,closest_hybrid=hybrid_message,destination=destination_name)
                        
                        session['vehicle_type']='taxi'
                        
                        return redirect(url_for('booking.select_taxi'))
                elif form_name == 'bus-form':
                        if session.get('closest_bus') is None:
                                return render_template('booking_select_destination.html',closest_bus=bus_message,closest_taxi=taxi_message,user_location=user_location,user_location_name=user_location_name,closest_hybrid=hybrid_message,destination=destination_name)
                        
                        session['vehicle_type']='bus'
                        
                        return redirect(url_for('booking.bus_options'))
                elif form_name == 'hybrid-form':
                        if session.get('closest_hybrid') is None:
                                return render_template('booking_select_destination.html',closest_bus=bus_message,closest_taxi=taxi_message,user_location=user_location,user_location_name=user_location_name,closest_hybrid=hybrid_message,destination=destination_name)
                        
                        session['vehicle_type']='hybrid'
                        
                        return redirect(url_for('booking.select_taxi'))
        return render_template('booking_select_destination.html',closest_bus=bus_message,closest_taxi=taxi_message,user_location=user_location,user_location_name=user_location_name,closest_hybrid=hybrid_message,destination=destination_name)





@bp.route('/booking/select_taxi',methods=['GET','POST'])
@login_required
def select_taxi():
        user_name=current_user.user_name

        bookings=Booking.query.filter_by(user_name=user_name).all()
        for booking in bookings:
                if booking.Status=="Pending":
                        return redirect(url_for('booking.wait'))
        print(user_name,'user name in select ride')
        phone_number=current_user.phone
        date=datetime.now().strftime("%Y-%m-%d")
        time=datetime.now().strftime("%H:%M:%S")
        destination=session.get('destination')
        vehicle_type=session.get('vehicle_type')
        if vehicle_type=='taxi':
                vehicle_no=session.get('closest_taxi')
                travel_time=session.get('taxi_travel_time')
        
                pickup_point=session.get('taxi_pickup_point')
                arrival_time=session.get('taxi_arrival_time')
        elif vehicle_type=='hybrid':
                vehicle_no=session.get('closest_hybrid')
                travel_time=session.get('hybrid_travel_time')
        
                pickup_point=session.get('hybrid_pickup_point')
                arrival_time=session.get('hybrid_arrival_time')
        
        print(vehicle_no,'vehicle no in select vehicle')
        
        fare=10
        
        
        if request.method=='POST':
                booking=Booking(user_name, phone_number, date, time, pickup_point, destination, vehicle_no, booking_type='taxi_ride')
                booking.save()
                booking_notification={'vehicle':vehicle_no,'destination':destination,'pickup_point':pickup_point,'rider':user_name,'timestamp':time,'booking_id':booking.id,'seen':False}
                session['booking']=booking_notification
                notifications.append(booking_notification)
                message = json.dumps(booking_notification)
                producer.send('booking_notification', value=message.encode())
                print(vehicle_no,'vehicle in booking')
                

                return redirect(url_for('booking.wait_confirmation'))
        

                



        return render_template('booking_select_taxi.html',travel_time=travel_time,fare=fare,vehicle_no=vehicle_no,arrival_time=arrival_time,pickup_point=pickup_point,destination=destination,vehicle_type=vehicle_type)

@bp.route('/booking/wait',methods=['GET','POST'])
@login_required
def wait():      
        bookings=Booking.query.filter_by(user_name=current_user.user_name).all()
        print(bookings,'bookings in wait')
        for booking in bookings:
                print(booking.Status,'status in wait')
                if booking.Status=="Pending":
                        return redirect(url_for('booking.wait_confirmation'))
                if booking.Status=="confirmed" and booking.payment_details:
                        if booking.payment_details.status=='pending':
                                return redirect(url_for('booking.wait_for_vehicle'))
                

        return render_template('booking_wait.html')                
                
@bp.route('/booking/bus_options',methods=['GET','POST'])
@login_required
def bus_options():
        buses=session.get('closest_bus')
        pickup_point=session.get('closest_stage')
        travel_time=session.get('travel_time')
        
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
                seats=(request.form.get('no_of_seats'))
                if seats is None or seats:
                        seats=1
                booked_seats=int(seats)
                no_plate=request.form.get('vehicle')
                no_plate=no_plate.strip()
                print(no_plate,'vehicle no in bus options')
                vehicle=Vehicle.query.filter_by(no_plate=no_plate).first()
                if vehicle is None:
                        error='Vehicle not found'
                        return render_template('booking_bus_options.html',buses=buses,pickup_point=pickup_point,destination=destination,travel_time=travel_time,error=error)
                        
                print(vehicle,'vehicle bus in bus options')
                
                
                booking=Booking(user_name, phone_number, date, time, pickup_point, destination, no_plate, booking_type='bus_ride')
                booking.save()
                booking_notification={'vehicle':no_plate,'destination':destination,'pickup_point':pickup_point,'rider':user_name,'timestamp':time,'date':date,'booking_id':booking.id,'no_of_seats':booked_seats,'seen':False}
                session['booking']=booking_notification
                notifications.append(booking_notification)
                message = json.dumps(booking_notification)
                producer.send('booking_notification', value=message.encode())
                print(no_plate,'vehicle in booking')
                
                return redirect(url_for('booking.wait_confirmation'))
                

        return render_template('booking_bus_options.html',buses=buses,pickup_point=pickup_point,destination=destination,travel_time=travel_time)




@bp.route('/booking/confirm',methods=['GET','POST'])
@login_required
@is_driver
def confirm_booking():
        vehicle=Vehicle.query.filter_by(driver_username=current_user.user_name).first()
        bookings=Booking.query.filter_by(vehicle_plate=vehicle.no_plate).all()
        details=[]

        date=datetime.now().strftime("%Y-%m-%d")
        dt1 = datetime.strptime(date, "%Y-%m-%d")
        for booking in bookings:
                if not booking.payment_details:
                        date2 = booking.date
                        
                        dt2 = datetime.strptime(date2, "%Y-%m-%d")
                        if dt1==dt2:
                                details.append(booking)
        
        notifications_messages=receive_notification(notifications,session.get('vehicle'))
        session['notifications']=notifications_messages
        

        
        if request.method=='POST':
                token = request.form.get('csrf_token')
                try:
                        validate_csrf(token)
                except ValidationError :
                        error="Invalid CSRF token"

                id=int(request.form.get('id'))
                
                
                print(id,'id in confirm booking')
                confirmation=request.form.get('confirmation')
                booking=Booking.query.filter_by(id=id).first()
                
                        
                if confirmation=='yes':
                        
                        booking.confirm()
                        session['passenger_location']=geocode(api_key,booking.pickup_point,booking)
                        session['passenger_destination']=geocode(api_key,booking.destination,booking)
                        

                else:
                        
                        booking.cancel()
                        
                                
                                      
                        
                return render_template('booking_confirm.html',details=details)
               

        return render_template('booking_confirm.html',details=details)




@bp.route('/booking/wait_confirmation',methods=['GET','POST'])
@login_required
def wait_confirmation():
        import time
        waiting_message='Your booking is in process. Please wait for confirmation.'
        booking_notification=session.get('booking')
        vehicle_no=session.get('booking')['vehicle']
        destination=session.get('booking')['destination']
        pickup_point=session.get('booking')['pickup_point']
        booking_id=session.get('booking')['booking_id']
        booking=Booking.query.filter_by(id=booking_id).first()
        if booking.Status=='confirmed':
                                        
                        return redirect(url_for('booking.wait_for_vehicle')) 
        elif booking.Status=='Cancelled':
                        
                        vehicle_type=session.get('vehicle_type')
                        if vehicle_type=='hire_car':
                                return redirect(url_for('hire.hire_car'))
                        elif vehicle_type=='hire_bus':
                                return redirect(url_for('hire.hire_bus'))
                        elif vehicle_type=='bus':
                                return redirect(url_for('booking.bus_options'))
                        elif vehicle_type=='taxi':
                                return redirect(url_for('booking.book_taxi'))
                        else:
                                return redirect(url_for('booking.book_hybrid'))
       
        if request.method=='POST':
                token = request.form.get('csrf_token')
                try:
                        validate_csrf(token)
                except ValidationError :
                        error="Invalid CSRF token"
                
                confirm=request.form.get('confirm')
        
        
                if confirm=='check':
                        while 1:
                                
                                print(booking.Status,'booking in check here')
                                if booking.Status=='confirmed':
                                                
                                                return redirect(url_for('booking.wait_for_vehicle')) 
                                elif booking.Status=='Cancelled':
                                                
                                                vehicle_type=session.get('vehicle_type')
                                                if vehicle_type=='hire_car':
                                                        return redirect(url_for('hire.hire_car'))
                                                elif vehicle_type=='hire_bus':
                                                        return redirect(url_for('hire.hire_bus'))
                                                elif vehicle_type=='bus':
                                                        return redirect(url_for('booking.bus_options'))
                                                elif vehicle_type=='taxi':
                                                        return redirect(url_for('booking.book_taxi'))
                                                else:
                                                        return redirect(url_for('booking.book_hybrid'))
                                else:
                                        waiting_message='Your booking is in process. Please wait for confirmation.'
                                        
                                                
                                if booking.type=='hire':
                                        time.sleep(6000)
                                else:
                                        time.sleep(10)
                                        
                else:
                        booking.cancel()
                        return redirect(url_for('booking.cancel_booking'))


                      
        return render_template('booking_wait_confirmation.html',booking_notification=booking_notification,waiting_message=waiting_message,vehicle_no=vehicle_no,destination=destination,pickup_point=pickup_point)


                



@bp.route('/booking/wait_for_vehicle',methods=['GET','POST'])
@login_required
def wait_for_vehicle():
    booking_id=session.get('booking')['booking_id']
    booking=Booking.query.filter_by(id=booking_id).first()
    user_name=current_user.user_name
    vehicle_no=session.get('booking')['vehicle']
    destination=session.get('booking')['destination']
    pickup_point=session.get('booking')['pickup_point']
    vehicle_type=session.get('vehicle_type')
    b_type='1'
    if vehicle_type=='taxi':
        session['vehicle_location']=session.get('taxi_location')
        wait_time=session.get('taxi_arrival_time')
        start_routing.delay()
    elif vehicle_type=='hybrid':
        session['vehicle_location']=session.get('hybrid_location')
        wait_time=session.get('hybrid_arrival_time')
        start_routing.delay()
    elif vehicle_type=='bus':
        session['vehicle_location']=session.get('bus_location')
        wait_time='bus leaves in a few minutes'
        start_routing.delay()
    else:
        
        pickup_point=booking.pickup_point
        wait_time=f'{booking.date} ,{booking.time}' 
        b_type='2'   
    if request.method=='POST':
            button=request.form.get('button')
            if button=='cancel':
                    booking.cancel()
                    return redirect(url_for('booking.cancel_booking'))
            else:
                    return redirect(url_for('payment.payment'))
                    
   
           
    
    
    return render_template('booking_wait_for_vehicle.html',b_type=b_type,user_name=user_name,wait_time=wait_time,vehicle_no=vehicle_no,destination=destination,pickup_point=pickup_point)

@bp.route('/booking/cancel_booking',methods=['GET','POST'])
@login_required
def cancel_booking():
        return render_template('booking_cancel.html')

           


@bp.route('/booking/review',methods=['GET','POST'])
@login_required
@is_driver
def review():
        return render_template('booking_review.html')



@bp.route('/booking/book_taxi',methods=['GET','POST'])
@login_required
def book_taxi():
        user_location=session.get('current_location',None)
        user_location_name=session.get('location_name',None)
        destination_name=session.get('destination')
       
        taxi_message=session.get('taxi_message',None)
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
                        taxi_data=create_kafka_objects(consumer_taxi)
                        print(taxi_data,'taxi data from kafka')
                        
                        destination_name=request.form.get('destination')
                        print(destination_name,'destination selected in form')
                        if destination_name=='':
                                error='Please select Destination'
                                return render_template('book_taxi.html',user_location=user_location,user_location_name=user_location_name,error=error)
                        session['destination']=destination_name
                        destination=geocode(api_key,destination_name,current_user)
                        if destination is None:
                                error='Check your Internet COnnection'
                                return render_template('book_taxi.html',user_location=user_location,user_location_name=user_location_name,error=error)
                        session['destination_coordinates']={'latitude':destination['latitude'],'longitude':destination['longitude']}
                        
                        if user_location is None or user_location=='':
                                error='Please select your location'
                                return render_template('book_taxi.html',error=error)
                        nearest_taxi=closest_taxi(user_location,taxi_data)
                        print(nearest_taxi,'nearest taxi in post')
                        if nearest_taxi is None:
                                my_taxi=None
                                taxi_message='No taxi nearby'
                        else:
                                print('we have a nearest taxi')
                                session['taxi_location']={'latitude':nearest_taxi[0]['latitude'],'longitude':nearest_taxi[0]['longitude']}
                                taxi_location_name=reverse_geocode(nearest_taxi[0]['latitude'], nearest_taxi[0]['longitude'])
                                session['taxi_location_name']=taxi_location_name
                                taxi_arrival_time=get_time(user_location_name, taxi_location_name,"driving", api_key)
                                session['taxi_arrival_time']=taxi_arrival_time
                                my_taxi=nearest_taxi[0]['vehicle']
                                taxi_message='Click here to book your taxi'
                                taxi_time=get_time(session.get('location_name'), destination_name,"driving", api_key)
                                print(taxi_time,'taxi time in post')
                                session['taxi_travel_time']=get_time(destination_name,session.get('location_name'),'driving',api_key)
                                print (session.get('taxi_travel_time'),'taxi travel time ')
                                session['taxi_pickup_point']=user_location_name

                
                        session['closest_taxi']=my_taxi
                        
                        session['pickup_point']=user_location_name
                
                        return render_template('book_taxi.html',closest_taxi=taxi_message,user_location=user_location,user_location_name=user_location_name)
                else :
                        
                        session['vehicle_type']='taxi'
                        
                        return redirect(url_for('booking.select_taxi'))
                
        return render_template('book_taxi.html',user_location=user_location,user_location_name=user_location_name,closest_taxi=taxi_message)



@bp.route('/booking/book_bus',methods=['GET','POST'])
@login_required
def book_bus():
        user_location=session.get('current_location')
        
        user_location_name=session.get('location_name',None)
        bus_message=session.get('bus_message',None)
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
                        old_bus_data=data = [
    {
        "vehicle": "EFG901",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-06-30 21:30:00",
        "bus_destination": "Nairobi CBD",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "HIJ234",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-06-30 22:45:00",
        "bus_destination": "Ruiru",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "KLM567",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-06-30 23:59:00",
        "bus_destination": "Ruiru",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "NOP890",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-07-01 01:15:00",
        "bus_destination": "Juja ",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "QRS123",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-07-01 02:30:00",
        "bus_destination": "Thika",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "ABC123",
        "latitude": -1.28639,
        "longitude": 36.8172,
        "timestamp": "2023-06-30 09:00:00",
        "bus_destination": "Juja",
        "docked": True,
        "docking_stage": "Nairobi CBD"
    },
    {
        "vehicle": "DEF456",
        "latitude": -1.23488,
        "longitude": 36.8892,
        "timestamp": "2023-06-30 10:15:00",
        "bus_destination": "Juja",
        "docked": True,
        "docking_stage": "Ruaraka (Getrude's Children's Hospital)"
    },
    {
        "vehicle": "GHI789",
        "latitude": -1.18699,
        "longitude": 36.9199,
        "timestamp": "2023-06-30 11:30:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kahawa West"
    },
    {
        "vehicle": "JKL012",
        "latitude": -1.21418,
        "longitude": 36.8907,
        "timestamp": "2023-06-30 12:45:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Roysambu"
    },
    {
        "vehicle": "MNO345",
        "latitude": -1.09793,
        "longitude": 37.0166,
        "timestamp": "2023-06-30 14:00:00",
        "docked": False,
        
    },
    {
        "vehicle": "PQR678",
        "latitude": -1.17554,
        "longitude": 36.9411,
        "timestamp": "2023-06-30 15:15:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kahawa Sukari"
    },
    {
        "vehicle": "STU901",
        "latitude": -1.22054,
        "longitude": 36.9029,
        "timestamp": "2023-06-30 16:30:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kasarani Sports Complex"
    },
    {
        "vehicle": "VWX234",
        "latitude": -1.14406,
        "longitude": 36.9608,
        "timestamp": "2023-06-30 17:45:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kenyatta University"
    },
    {
        "vehicle": "YZA567",
        "latitude": -1.18345,
        "longitude": 36.9272,
        "timestamp": "2023-06-30 19:00:00",
        "bus_destination": "Nairobi",
        "docked": True,
        "docking_stage": "Kahawa Wendani"
    },
    {
        "vehicle": "BCD890",
        "latitude": -1.03867,
        "longitude": 37.0768,
        "timestamp": "2023-06-30 20:15:00",
        "docked": False,
        
    }
]

                        print(old_bus_data,'bus data fro kafka')
                        bus_data = [bus for bus in old_bus_data if bus['docked']]
                        
                        destination_name=request.form.get('destination')
                        print(destination_name,'destination selected in form')
                        if destination_name=='':
                                error='Please select Destination'
                                return render_template('book_bus.html',user_location=user_location,user_location_name=user_location_name,error=error)
                        session['destination']=destination_name
                        destination=geocode(api_key,destination_name,current_user)
                        if destination is None:
                                error='Check your Internet COnnection'
                                return render_template('book_bus.html',user_location=user_location,user_location_name=user_location_name,error=error)
                        session['destination_coordinates']={'latitude':destination['latitude'],'longitude':destination['longitude']}
                        
                        
                        nearest_stage=closest_stage(user_location)
                        print(nearest_stage[0]['stage_name'],'nearest stage to user')
                        if user_location is None or user_location=='':
                                error='Please select your location'
                                return render_template('book_bus.html',error=error)
                        
                        user_time=get_time(session.get('location_name'), nearest_stage[0]['stage_name'],"walking", api_key)
                        print(f"{user_time} Time needed for user to walk to stage {nearest_stage[0]['stage_name']}")
                        bus_time=get_time(nearest_stage[0]['stage_name'], destination_name,"driving", api_key)
                        print(f"{bus_time} Total time for user to get to destination on bus")
                        session['travel_time']=bus_time

                        routed_bus_data=find_route(bus_data)
                        viable_buses=allow_passenger(routed_bus_data,destination_name,nearest_stage[0]['stage_name'])

                        a_bus=bus(viable_buses)
                        if a_bus is None:
                                bus_message='No bus nearby'
                                

                        else:
                                
                                #bus_location_name=reverse_geocode(a_bus[0]['latitude'], a_bus[0]['longitude'])
                                #bus_arrival_time=get_time(nearest_stage[0]['stage_name'], bus_location_name,"driving", api_key)
                                #my_bus=a_bus[0]['vehicle']
                                
                                bus_message='Click here to select a bus'
                                session['user_to_stage_time']=user_time
                                session['bus_travel_time']=get_time(nearest_stage[0]['stage_name'],destination_name,'driving',api_key)
                        print(a_bus,'a bus in post')
                        session['bus_location']={'latitude':nearest_stage[0]['latitude'],'longitude':nearest_stage[0]['longitude']}
                        session['closest_bus']=a_bus
                        session['closest_stage']=nearest_stage[0]['stage_name']
                        session['pickup_point']=nearest_stage[0]['stage_name']
                
                        return render_template('book_bus.html',closest_bus=bus_message,user_location=user_location,user_location_name=user_location_name)
                
        
                else:
                        
                        session['vehicle_type']='bus'
                        
                        return redirect(url_for('booking.bus_options'))
               
        return render_template('book_bus.html',user_location=user_location,user_location_name=user_location_name,closest_bus=bus_message)


@bp.route('/booking/book_hybrid', methods=('GET', 'POST'))
@login_required
def book_hybrid():      
        user_location=session.get('current_location')
        print(user_location,'user location in select destination')
        
        user_location_name=session.get('location_name',None)
        hybrid_message=session.get('hybrid_message',None)
        
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
                        hybrid_data=create_kafka_objects(consumer_hybrid)
                        print(hybrid_data,'hybrid data from kafka')
                        
                        destination_name=request.form.get('destination')
                        print(destination_name,'destination selected in form')
                        if destination_name=='':
                                error='Please select Destination'
                                return render_template('book_hybrid.html',user_location=user_location,user_location_name=user_location_name,error=error)
                        session['destination']=destination_name
                        destination=geocode(api_key,destination_name,current_user)
                        if destination is None:
                                error='Check your Internet COnnection'
                                return render_template('book_hybrid.html',user_location=user_location,user_location_name=user_location_name,error=error)
                        session['destination_coordinates']={'latitude':destination['latitude'],'longitude':destination['longitude']}
                        
                        
                        nearest_stage=closest_stage(user_location)
                        print(nearest_stage[0]['stage_name'],'nearest stage to user')
                        if user_location is None or user_location=='':
                                error='Please select your location'
                                return render_template('book_hybrid.html',error=error)
                        nearest_hybrid_to_user=closest_taxi(user_location,hybrid_data)
                        
                        print(nearest_hybrid_to_user,'nearest hybrid to user')
                        
                        if nearest_hybrid_to_user is None:
                                nearest_hybrid_to_stage=find_closest_hybrid_to_stage(nearest_stage[0]['latitude'],nearest_stage[0]['longitude'],hybrid_data)
                                my_hybrid=nearest_hybrid_to_stage
                                print(nearest_hybrid_to_stage,'nearest hybrid to stage')
                                if my_hybrid is None or len(my_hybrid)==0:
                                        print('no hybrid nearby')
                                        hybrid_message='No hybrid nearby'
                                        return render_template('book_hybrid.html',user_location=user_location,user_location_name=user_location_name,closest_hybrid=closest_hybrid)
                                else:
                                        my_hybrid=nearest_hybrid_to_user
                                        hybrid_location_name=reverse_geocode(my_hybrid[0]['latitude'], my_hybrid[0]['longitude'])
                                        session['hybrid_location_name']=hybrid_location_name
                                        hybrid_arrival_time=get_time(nearest_stage[0]['stage_name'], hybrid_location_name,"driving", api_key)
                                        hybrid_time=get_time(nearest_stage[0]['stage_name'], destination_name,"driving", api_key)
                                        session['hybrid_pickup_point']=nearest_stage[0]['stage_name']
                                        my_hybrid_now=my_hybrid[0]['vehicle']
                                        session['hybrid_arrival_time']=hybrid_arrival_time
                                        hybrid_message='Click here to share your ride'
                        else:
                                my_hybrid=nearest_hybrid_to_user
                                hybrid_location_name=reverse_geocode(my_hybrid[0]['latitude'], my_hybrid[0]['longitude'])
                                session['hybrid_location_name']=hybrid_location_name
                                hybrid_arrival_time=get_time(user_location_name, hybrid_location_name,"driving", api_key)
                                hybrid_time=get_time(session.get('location_name'), destination_name,"driving", api_key)
                                session['hybrid_pickup_point']=user_location_name
                                session['hybrid_arrival_time']=hybrid_arrival_time
                                my_hybrid_now=my_hybrid[0]['vehicle']
                        
                                hybrid_message='Click here to share your ride'
                        
                                print(hybrid_time,'hybrid time in post')
                        session['hybrid_location']={'latitude':my_hybrid[0]['latitude'],'longitude': my_hybrid[0]['longitude']}
                        session['hybrid_message']=hybrid_message
                        session['hybrid_travel_time']=hybrid_time
                        print (session.get('hybrid_travel_time'),'hybrid travel time ')
                        
                        
                        
                        
                        session['closest_hybrid']=my_hybrid_now
                        session['closest_stage']=nearest_stage[0]['stage_name']
                
                        return render_template('book_hybrid.html',user_location=user_location,user_location_name=user_location_name,hybrid_message=hybrid_message)
                
                else:
                        session['vehicle_type']='hybrid'
                        return redirect(url_for('booking.select_taxi'))
        return render_template('book_hybrid.html',user_location=user_location,user_location_name=user_location_name,hybrid_message=hybrid_message)
