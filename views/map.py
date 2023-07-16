from flask import render_template,Blueprint,session
from flask_googlemaps import Map
from flask_login import login_required,current_user
from models.user import User





bp=Blueprint('map',__name__)

@bp.route('/map/user')
@login_required
def location():
    user=User.query.filter_by(user_name=current_user.user_name).first()
    if user.driver_details:
        user_location=session.get('passenger_location',None)
        destination=session.get('passenger_destination',None)
    else:
        user_location=session.get('vehicle_location',None)
        print(user_location,'in map')
        destination=session.get('destination_coordinates',None)
        print(destination,'in map')
    return render_template('location_user.html',user_location=user_location,destination=destination)


    
   