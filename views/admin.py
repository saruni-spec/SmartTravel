from flask import Blueprint,render_template
from models.vehicle import Vehicle
from models.booking import Booking
from models.user import User
from models.driver import Driver
from models.stages import Stages
from flask_login import login_required,current_user


bp=Blueprint('admin',__name__)

@bp.route('/admin/vehicles')
@login_required
def vehicles():
    vehicles=Vehicle.query.all()

    return render_template('admin_vehicles.html',vehicles=vehicles)

@bp.route('/admin/bookings')
@login_required
def booking_details(booking):
    booking=Booking.query.all()
    return render_template('admin_bookings.html',booking=booking)

@bp.route('/admin/users')
@login_required
def users():
    users=User.query.all()
    return render_template('admin_users.html',users=users)

@bp.route('/admin/drivers')
@login_required
def drivers():
    drivers=Driver.query.all()
    return render_template('admin_drivers.html',drivers=drivers)

@bp.route('/admin/stages')
@login_required
def stages():
    stages=Stages.query.all()
    return render_template('admin_stages.html',stages=stages)