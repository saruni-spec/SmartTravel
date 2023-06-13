from flask import render_template,Blueprint,current_app,request
from flask_googlemaps import Map

bp=Blueprint('map',__name__)

@bp.route('/map/location')
def mapview():
    return render_template('location_map.html')

@bp.route('/map/user')
def user_location():
        return render_template('location_user.html')
    
   