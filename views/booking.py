from flask import render_template,Blueprint,session
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
from extensions.celery import process_notifications,Notofications


from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError


from models.kafka import *
from flask_login import login_required
from .profile import is_driver






consumer_bus = KafkaConsumer('bus_coordinates',group_id='my-group',bootstrap_servers=['localhost:9092'],consumer_timeout_ms=10000)
consumer_taxi=KafkaConsumer('bus_coordinates',group_id='my-group-taxi',bootstrap_servers=['localhost:9092'],consumer_timeout_ms=10000 )
producer = KafkaProducer(bootstrap_servers='localhost:9092')


            


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
    
        destination_lat = float(closest_taxi['latitude'])
        destination_lng = float(closest_taxi['longitude'])
        distance = get_distance(latitude, longitude, destination_lat, destination_lng)
        return[closest_taxi,distance]

def closest_bus(closest_stage,bus_data):
        bus_clusters=group_coordinates(bus_data, 5)
        print(bus_clusters,'closest bus')
        latitude = float(closest_stage[0]['latitude']) 
        longitude = float(closest_stage[0]['longitude'])
        print(latitude,longitude ,'in closest bus')
        closest_bus=(find_closest_bus(latitude, longitude, bus_clusters,closest_stage[1]))
        print(closest_bus,'closest bus in none toye!!!!!')
        if closest_bus is None:
                destination_lat = -1.1
                destination_lng = 36.9
        else:
                destination_lat = float(closest_bus['latitude'])
                destination_lng = float(closest_bus['longitude'])
        distance = get_distance(latitude, longitude, destination_lat, destination_lng)
        return[closest_bus,distance]


def bus(closest_stage,bus_data,destination,bus_location,user_time,bus_time):
        bus_clusters=group_coordinates(bus_data, 5)
        print(bus_clusters,'closest bus')
        latitude = float(closest_stage[0]['latitude']) 
        longitude = float(closest_stage[0]['longitude'])
        print(latitude,longitude ,'in closest bus')
        closest_bus=(find_bus(bus_clusters,destination,bus_location,user_time,bus_time))
        if closest_bus is None:
                destination_lat = -1.1
                destination_lng = 36.9
        else:
                destination_lat = float(closest_bus['latitude'])
                destination_lng = float(closest_bus['longitude'])
        distance = get_distance(latitude, longitude, destination_lat, destination_lng)
        return[closest_bus,distance]



def get_time(origin_location, destination_location, travel_mode, api_key):
    print(origin_location,'origin location')
    print(destination_location,'destination location')
    print(travel_mode,'travel mode')
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_location}&destination={destination_location}&mode={travel_mode}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        route = data['routes'][0]
        leg = route['legs'][0]
        duration = leg['duration']['text']
        print(duration,'duration')
        return duration
    else:
        return None

bp=Blueprint('booking',__name__)

@bp.route('/booking/select_destination',methods=['GET','POST'])  
@login_required
def select_destination():
        bus_data=create_kafka_objects(consumer_bus)
        print(bus_data,'bus data')
        taxi_data=create_kafka_objects(consumer_taxi)
        print(taxi_data,'taxi data')
        user_location=session.get('current_location')
        if user_location is None:
                user_location={'user':current_user.user_name,'latitude':-1.1,'longitude':36.9}
        print(user_location,'user location in post up')
        print(jsonify(user_location),'user location in jsonify up')
        if request.method=='POST':
                destination=request.form.get('destination')
                session['destination']=destination
                import requests

                api_key = "AIzaSyA_JxBRmUKjcpPLWXwAagTX9k19tIWi2SQ"

                url = f"https://maps.googleapis.com/maps/api/geocode/json?address={destination}&key={api_key}"
                response = requests.get(url)
                data = response.json()
                if data['status'] == 'OK':
                        result = data['results'][0]
                        location = result['geometry']['location']
                        latitude = location['lat']
                        longitude = location['lng']
                        destination={'location':destination,'latitude':latitude,'longitude':longitude,'user':current_user.user_name}
                else:
                        Error= "Unable to retrieve coordinates."

                
                nearest_stage=closest_stage(user_location)
                
                session['stage_name']=nearest_stage
                print(nearest_stage,'nearest stage in post')
                print(taxi_data,'taxi_data')
                nearest_taxi=closest_taxi(user_location,taxi_data)
                print(nearest_taxi,'nearest taxi in post')
                nearest_bus=closest_bus(nearest_stage,bus_data)
                print(user_location,'user location in post')
                print(nearest_bus,'nearest bus in post')
                bus_time=get_time(session.get('location_name'), destination['location'],"driving", api_key)
                print(bus_time,'bus time in post')
                user_time=get_time(session.get('location_name'), nearest_stage[0]['stage_name'],"walking", api_key)
                print(user_time,'user time in post')
                session['pickup_point']=[nearest_stage[0]['stage_name'],user_location]
                a_bus=bus(nearest_stage,bus_data,destination,user_location,user_time,bus_time)
                print(a_bus,'a bus in post')
                session['closest_bus']='fgt'
                session['closest_taxi']='fgt'
               
                return render_template('booking_select_destination.html',closest_bus='fgt',bus_time=bus_time,closest_stage=nearest_stage[0]['stage_name'],user_time=user_time,closest_taxi='fgt',user_location=user_location)
        
        

        return render_template('booking_select_destination.html',user_location=user_location,user_name='')



notifications=[]

@bp.route('/booking/select_vehicle',methods=['GET','POST'])
@login_required
def select_vehicle():
        
        if request.method=='POST':
                user_name=current_user.user_name
                print(user_name,'user name in select vehicle')
                phone_number='888'
                date=datetime.now().strftime("%Y-%m-%d")
                time=datetime.now().strftime("%H:%M:%S")
                destination=session.get('destination')
                vehicle_no=session.get('closest_bus')
                print(vehicle_no,'vehicle no in select vehicle')
                vehicle_type=Vehicle.query.filter_by(no_plate=vehicle_no).first()
                pickup_point=session.get('pickup_point')
                Fare=10
                booking=Booking(user_name, phone_number, date, time, pickup_point[0], destination, vehicle_no, Fare)
                booking.save()
                booking_notification={'vehicle':vehicle_no,'destination':destination,'pickup_point':pickup_point,'rider':user_name,'timestamp':time}
                notifications.append(booking_notification)
                message = json.dumps({'vehicle':vehicle_no,'destination':destination,'pickup_point':pickup_point,'rider':user_name,'timestamp':time})
                producer.send('booking_notification', value=message.encode())
                print(vehicle_no,'vehicle in bookind')
                if booking.Status=='Confirmed':
                        waiting_message='Booking confirmed'
                elif booking.Status=='Cancelled':
                        waiting_message='Booking cancelled'
                else:
                        waiting_message='WAiting for confirmation'



                return render_template('booking_select_vehicle.html',waiting_message=waiting_message,vehicle_no=vehicle_no)
        

                



        return render_template('booking_select_vehicle.html')



from datetime import datetime, timedelta
def receive_notification(notifications ,current_vehicle):
        current_time = datetime.now()
        for notification in notifications:
            if notification['vehicle']==current_vehicle:
                timestamp = datetime.strptime(notification['timestamp'], "%H:%M:%S")
                time_difference = current_time - timestamp
                if time_difference > timedelta(minutes=3):
                    print(notification,'sent to driver')

                    return notification
            else:
                return None
            

@bp.route('/booking/confirm',methods=['GET','POST'])
@login_required
@is_driver
def confirm_booking():
        details=[]
        details.append(receive_notification(notifications,session.get('vehicle')))
        print(details,'details in confirm')

        if request.method=='POST':
                token = request.form.get('csrf_token')
                try:
                        validate_csrf(token)
                except ValidationError :
                        error="Invalid CSRF token"
                confirmation=request.form.get('confirmation')
                booking=Booking.query.filter_by(user_name=details[0]['rider']).first()
                if confirmation=='yes':
                        
                        booking.confirm()
                        
                        return render_template('booking_confirm.html',details=details,confirmed_message='Booking confirmed')

                else:
                
                        booking.cancel()
                return render_template('booking_confirm.html',details=details,confirmed_message='Booking cancelled')

        return render_template('booking_confirm.html',details=details)