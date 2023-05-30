from flask import render_template,Blueprint,current_app,request
from flask_googlemaps import Map

bp=Blueprint('map',__name__)

@bp.route('/map')
def mapview():
    return render_template('map.html')

@bp.route('/location')
def user_location():
        return render_template('location.html')
    
   