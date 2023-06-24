from flask import render_template,Blueprint,current_app,request
from flask_googlemaps import Map

bp=Blueprint('map',__name__)

@bp.route('/map/user')
def mapview():
    return render_template('location_user.html')

@bp.route('/map/location')
def user_location():
        return render_template('location_map.html')
    
   