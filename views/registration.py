from flask import render_template,Blueprint,current_app,session,make_response
from flask import request,redirect
from models.user import User
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required,current_user,login_user,logout_user
from logic.validation import *
from flask_mail import Message
from models.vehicle import Vehicle
from models.user import User
from flask import url_for
from models.driver import Driver
from datetime import timedelta




bp=Blueprint('registration',__name__)

@bp.route('/registration/rider',methods=['GET','POST'])
def registration():
    with current_app.app_context():
        error=None
        if request.method=='POST':
            token = request.form.get('csrf_token')
            try:
                validate_csrf(token)
            except ValidationError :
                return 'invalid csrf',404

            user_name=request.form.get('user_name')
            user=User.query.filter_by(user_name=user_name).first()
            if user:
                error="user_name already exists"
                return render_template('registration_rider.html',error=error) 
            
            password=request.form.get('password')
            first_name=request.form.get('first_name')
            other_name=request.form.get('other_name')
            email=request.form.get('email')

            error=validate_email(email)
            if error:
                return render_template('registration_rider.html',error=error)
            
            user=User.query.filter_by(email=email).first()
            if user:
                error="email already exists"
                return render_template('registration_rider.html',error=error)
            
            error=validate_password(password)
            if error is None:
                user=User(user_name)
                print(user_name,'username ')
                print(password,'password')
                user.save(password,first_name,other_name,email)
                print("User created")
                driver=request.form.get('driver')
                if driver=='yes':
                    return redirect(url_for('registration.login'))
                else:
                    return redirect(url_for('login.login'))
            else:
                return render_template('registration_rider.html',error=error)
        return render_template('registration_rider.html')
    

@bp.route('/registration/vehicle',methods=['GET','POST'])
@login_required
def register_vehicle():
    from models.owner import Owner
    with current_app.app_context():
        error=None
        if request.method=='POST':
            token=request.form.get('csrf_token')
            try:
                validate_csrf(token)
            except ValidationError:
                error="Invalid CSRF token"

            id_no = request.form.get('id_no')
            no_plate = request.form.get('no_plate')
            vehicle_type = request.form.get('vehicle_type')
            capacity = request.form.get('capacity')
            color=request.form.get('color')
            build_type=request.form.get('build_type')

            vehicle=Vehicle.query.filter_by(no_plate=no_plate).first()
            if vehicle:
                error="vehicle already exists"
                return render_template('registration_vehicle.html',error=error)
            else:
                vehicle=Vehicle(no_plate)
                owner=Owner.query.filter_by(user_name=current_user.user_name).first()
                if owner is None:
                    owner=Owner(current_user.user_name,id_no)
                    owner.save()
                    user=User.query.filter_by(user_name=current_user.user_name).first()
                    user.make_owner()
                vehicle.save(vehicle_type,current_user.user_name,capacity,color,build_type)

           
            

            return redirect('/registration/vehicle/driver')

            
            


        return render_template('registration_vehicle.html')


@bp.route('/registration/vehicle/driver',methods=['GET','POST'])
@login_required
def register_vehicle_driver():
    
    user=User.query.filter_by(user_name=current_user.user_name).first()
    vehicle=Vehicle.query.filter_by(owner_username=current_user.user_name).first()
    with current_app.app_context():
        from app import mail
        error=None
        if request.method=='POST':
            if 'next' in request.form:

                
                contact=request.form.get('email')
                if contact is None or contact=='':
                    contact=user.email
                    
                
                
                error=validate_email(contact)
                if error is None:
                    with open('/home/boss/SmartTravel/templates/confirmation.html', 'r') as f:
                            html_content = f.read()
                    verification_code=generate_verification_code()
                    message = Message('Confirmation Code', recipients=[contact])
                    message.html = html_content.format(verification_code=verification_code)
                    mail.send(message)

                    vehicle.add_verification_code(verification_code)
                    
                    
                    return redirect(url_for('registration.success'))
                else:
                    return render_template('registration_add_driver.html',error=error)
                
            elif 'skip':
                user.make_driver()
                
                
                return redirect(url_for('registration.success'))
        return render_template('registration_add_driver.html')


@bp.route('/registration/driver',methods=['GET','POST'])
def register_driver():
    from models.driver import Driver
    user=User.query.filter_by(user_name=current_user.user_name).first()
    with current_app.app_context():
        error=None
    
        if request.method=='POST':
            
            license=request.form.get('license_no')
            if license is None or license=='':
                return render_template('registration_driver.html',error="Enter License Number")
            phone=request.form.get('phone_no')
            if phone is None or phone=='':
                return render_template('registration_driver.html',error="Enter Phone Number")
            user.add_phone(phone)
            driver=Driver(current_user.user_name,license)
            driver.save()
            user.make_driver()
            return redirect(url_for('registration.vehicle_registration'))
            
        return render_template('registration_driver.html')
    
@bp.route('/registration/driver_registration',methods=['GET','POST'])
def driver_registration():
    return render_template('registration_for_driver.html')

@bp.route('/registration/vehicle_registration',methods=['GET','POST'])
def vehicle_registration():
    return render_template('registration_for_vehicle.html')

@bp.route('/registration/verify_vehicle',methods=['GET','POST'])
def verify_vehicle():
    if request.method=='POST':
        verification_code=request.form.get('verification_code')
        no_plate=request.form.get('no_plate')
        vehicle=Vehicle.query.filter_by(no_plate=no_plate).first()
        if vehicle:
            if vehicle.verification_code==verification_code:
                vehicle.change_driver(current_user.user_name)
                return redirect(url_for('registration.success'))
            else:
                error="Invalid Verification Code"
                return render_template('verify_vehicle.html',error=error)
        else:
            return render_template('verify_vehicle.html',error="Invalid Verification Code")
    return render_template('verify_vehicle.html')



@bp.route('/registration/login',methods=['GET','POST'])
def login():
    with current_app.app_context():
        error=None
        if request.method=='POST':
            token = request.form.get('csrf_token')
            try:
                validate_csrf(token)
            except ValidationError :
                error="Invalid CSRF token"
                return error,404
            
            username=request.form.get('username')
            password=request.form.get('password')
            user = User.query.filter_by(user_name=username).first()
            if not user:
                user=User.query.filter_by(email=username).first()
                if not user:
                    error='Invalid User'
                    return render_template('registration_driver_login.html',error=error)
            
            
            if user and user.verify_password(password):
                login_user(user)
                session['current_user']=current_user.user_name

                response = make_response(redirect(url_for('registration.register_driver')))
                response.set_cookie('username', username, max_age=timedelta(days=1))
                return response
            elif  user and not user.verify_password(password):
                error='Invaid Password'
                return render_template('registration_driver_login.html',error=error)
            else:
                error='Invalid User'
                return render_template('registration_driver_login.html',error=error)
    return render_template('registration_driver_login.html')

@bp.route('/registration/success',methods=['GET','POST'])
def success():
    if request.method=='POST':
       
        return redirect(url_for('login.logout'))
    return render_template('registration_success.html')