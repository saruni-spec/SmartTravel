from flask import Blueprint,render_template
from models.stages import Stages
from logic.matching import *
from logic.routing import *
from flask_login import login_required




bp=Blueprint('reg_stages',__name__)

@bp.route('/reg_stages',methods=['GET','POST'])
def reg_stages():
    
    stages_data = Stages.query.all()
    stage_clusters=group_coordinates(stages_data, 5)
    closest_stage=(find_closest_bus_stop(-1.1781268, 36.9364686, stage_clusters))
    origin_lat = -1.1781268
    origin_lng = 36.9364686
    destination_lat = closest_stage.latitude
    destination_lng = closest_stage.longitude
    distance = get_distance(origin_lat, origin_lng, destination_lat, destination_lng)
    print('Distance:', distance,":",closest_stage.stage_name)
    return render_template('reg_stages.html')


@bp.route('/reg_stages/route',methods=['GET','POST'])
@login_required
def reg_stages_route():
    from models.routes import Route
    
    route = Route(1)
    print(route.id,'route_id')
    print(route.stages,'route_stages')
    distance=calculate_route_distance(route)
    print(distance,'longest_distance')
    route.distane(distance)
    return render_template('reg_stages_route.html')