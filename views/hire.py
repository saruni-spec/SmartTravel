from flask import Blueprint,render_template ,redirect
from flask_login import login_required,current_user
from models.vehicle import Vehicle 

bp=Blueprint('hire',__name__)

@bp.route('/hire/car' ,methods=['GET','POST'])
@login_required
def hire_car():
    vehicle=Vehicle.query.filter_by(for_hire=True).all()
    listed_cars=[]
    for car in vehicle:
        if vehicle.vehicle_type=="taxi" or vehicle.vehicle_type=="hybrid":

            
            listed_cars.append(car)
    if len(listed_cars)==0:
        listed_cars=None
    return render_template('hire_car.html',cars=listed_cars)

@bp.route('/hire/bus',methods=['GET','POST'])
@login_required
def hire_bus():
    vehicle=Vehicle.query.filter_by(for_hire=True).all()
    listed_cars=[]
    for car in vehicle:
        if vehicle.vehicle_type=="bus":

            
            listed_cars.append(car)
    if len(listed_cars)==0:
        listed_cars=None
    return render_template('hire_bus.html',cars=listed_cars)