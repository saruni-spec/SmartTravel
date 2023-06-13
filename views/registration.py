from flask import render_template,Blueprint,current_app,session
from flask import request,redirect
from models.user import User
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required,current_user
from logic.validation import *
from flask_mail import Message
from models.vehicle import Vehicle





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
                error="Invalid CSRF token"
            username=request.form['username']
            password=request.form['password']
            error=validate_password(password)
            if error is None:
                user=User(username)
                print(username,'username ')
                print(password,'password')
                user.save(password)
                print("User created")
                return redirect('/login')
            else:
                return render_template('registration_rider.html',error=error)
        return render_template('registration_rider.html')
    

@bp.route('/registration/vehicle',methods=['GET','POST'])
@login_required
def register_vehicle():
    
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

            
            session['id_no']=id_no
            session['no_plate']=no_plate
            session['vehicle_type']=vehicle_type
            session['capacity']=capacity
            session['color']=color

            return redirect('/registration/vehicle/driver')

            
            


        return render_template('registration_vehicle.html')


@bp.route('/registration/vehicle/driver',methods=['GET','POST'])
@login_required
def register_vehicle_driver():
    
    from models.owner import Owner
    with current_app.app_context():
        from app import mail
        error=None
        if request.method=='POST':
            if 'next' in request.form:
                token=request.form.get('csrf_token')
                print('registering driver')
                try:
                    validate_csrf(token)
                except ValidationError:
                    error="Invalid CSRF token"
                
                driver_contact=request.form.get('email')
                error=validate_email(driver_contact)
                if error is None:
                    with open('/home/boss/SmartTravel/templates/confirmation.html', 'r') as f:
                            html_content = f.read()
                    verification_code=generate_verification_code()
                    message = Message('Confirmation Code', recipients=[driver_contact])
                    message.html = html_content.format(verification_code=verification_code)
                    mail.send(message)
                    owner=Owner(current_user.user_name,session.get('id_no'))
                    owner.save()
                    vehicle=Vehicle(session.get('no_plate'))
                    print(session.get('vehicle_type'),current_user.user_name,None,session.get('capacity'),session.get('color'),verification_code)
                    vehicle.save(session.get('vehicle_type'),current_user.user_name,None,session.get('capacity'),session.get('color'),verification_code)
                    
                    return redirect('/profile/owner')
                else:
                    return render_template('registration_add_driver.html',error=error)
            elif 'skip':
                token=request.form.get('csrf_token')
                print('registering driver')
                try:
                    validate_csrf(token)
                except ValidationError:
                    error="Invalid CSRF token"
                
                with open('/home/boss/SmartTravel/templates/confirmation.html', 'r') as f:
                            html_content = f.read()
                verification_code=generate_verification_code()
                message = Message('Confirmation Code', recipients=[current_user.email])
                message.html = html_content.format(verification_code=verification_code)
                mail.send(message)
                owner=Owner(current_user.user_name,session.get('id_no'))
                owner.save()
                vehicle=Vehicle(session.get('no_plate'))
                vehicle.save(session.get('vehicle_type'),current_user.user_name,current_user.user_name,session.get('capacity'),session.get('color'),verification_code)
                
                return redirect('/profile/driver')
        return render_template('registration_add_driver.html')


@bp.route('/registration/driver',methods=['GET','POST'])
@login_required
def register_driver():
    from models.driver import Driver
    with current_app.app_context():
        error=None
    
        if request.method=='POST':
            token=request.form.get('csrf_token')
            try:
                validate_csrf(token)
            except ValidationError:
                error="Invalid CSRF token"
            verification_code=request.form.get('verification_code')
            vehicle=Vehicle.query.filter_by(verification_code=verification_code).first()
            if vehicle is not None:
                driver_email=request.form.get('email')
                error=validate_email(driver_email)
                if error is None:
                    current_user.add_email(driver_email)
                    current_user.add_phone(request.form.get('phone_no'))
                    driver=Driver(current_user.user_name,request.form.get('license_no'))
                    driver.save()
                    return redirect('/profile/driver')
                else:
                    return render_template('registration_driver.html',error=error)
            else:
                return render_template('registration_driver.html',error="Invalid Verification Code")
        return render_template('registration_driver.html')

@bp.route('/logout')
def logout():   
    session.clear()
    return redirect('login')