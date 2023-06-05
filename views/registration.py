from flask import render_template,Blueprint,current_app,session
from flask import request,redirect
from models.user import User
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from flask_login import login_required
from logic.validation import validate_password,validate_email





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
                session['username']=username
                session['password']=password
                return redirect('login')
            else:
                return render_template('registration_rider.html',error=error)
        return render_template('registration_rider.html')
    

@bp.route('/registration/vehicle',methods=['GET','POST'])
@login_required
def register_vehicle():
    from models.vehicle import Vehicle
    with current_app.app_context():
        error=None
        if request.method=='POST':
            token=request.form.get('csrf_token')
            try:
                validate_csrf(token)
            except ValidationError:
                error="Invalid CSRF token"
            owner=session.get('user_id')
            id_no = request.form.get('id_no')
            no_plate = request.form.get('no_plate')
            make = request.form.get('make')
            capacity = request.form.get('capacity')
            color=request.form.get('color')
            driver=request.form.get('driver')
            if driver is None or  driver=='' or driver=='self' or driver=='Self' or driver==owner:
                driver=owner
                print(owner,"owner")
                print(driver,"driver 1")
                user=User.query.filter_by(user_name=driver).first()
                user.make_driver()
                user.make_owner()
            else:
                driver=User.query.filter_by(user_name=driver).first()
                if driver is None:
                    error="Driver not found"
                    return render_template('registration_vehicle.html',error=error)
                else:
                    print(driver,"driver 2")
                    driver.make_driver()
                    owner=User.query.filter_by(user_name=owner).first()
                    owner.make_owner()
            vehicle=Vehicle(no_plate)
            vehicle.save(make,owner,driver,capacity,color)


        return render_template('registration_vehicle.html')


@bp.route('/registration/driver',methods=['GET','POST'])
def register_driver():
    with current_app.app_context():
        error=None
        if request.method=='POST':
            token=request.form.get('csrf_token')
            print('registering driver')
            try:
                validate_csrf(token)
            except ValidationError:
                error="Invalid CSRF token"
            driver_name=request.form.get('username')
            driver_contact=request.form.get('email')
            error=validate_email(driver_contact)
            if error is None:
                password=request.form.get('password')
                error=validate_password(password)
                if error is None:
                    user=User.query.filter_by(user_name=driver_name).first()
                    if user is not None:
                        print('old user inr driver')
                        user.make_driver()
                        user.add_email(driver_contact)
                        return redirect('/login')
                    else:
                        print('new user inr driver')
                        
                        driver=User(driver_name)
                        driver.save(password)
                        driver.make_driver()
                        driver.add_email(driver_contact)
                        return redirect('/login')
                else:
                    return render_template('registration_driver.html',error=error)
            else:
                return render_template('registration_driver.html',error=error)
        return render_template('registration_driver.html')




@bp.route('/logout')
def logout():   
    session.clear()
    return redirect('login')