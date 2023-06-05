from flask import render_template,Blueprint,session
from datetime import datetime
from flask import request
from logic.matching import *
from logic.routing import *
from models.stages import Stages





bp=Blueprint('booking',__name__)

@bp.route('/booking/select_vehicle',methods=['GET','POST'])  
def book():
       
        stages_data = Stages.query.all()
        stage_clusters=group_coordinates(stages_data, 5)
        user_location=session.get('current_location')
        print(user_location,'llll')
        latitude=float(user_location['latitude'])
        longitude=float(user_location['longitude'])
        print(latitude,longitude)
        closest_stage=(find_closest_bus_stop(latitude, longitude, stage_clusters))
    
        destination_lat = float(closest_stage.latitude)
        destination_lng = float(closest_stage.longitude)
        distance = get_distance(latitude, longitude, destination_lat, destination_lng)
        print('Distance:', distance,":",closest_stage.stage_name,"is the closest stage")
        return render_template('booking_select_vehicle.html')