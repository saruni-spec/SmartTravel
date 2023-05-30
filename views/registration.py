from flask import render_template,Blueprint,current_app,session
from flask import request,redirect
from models.user import User
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError


bp=Blueprint('registration',__name__)


def validate_password(password):
        if len(password) < 12:
            return "Password must be at least 12 characters long."
        elif not any(char.isdigit() for char in password):
            return "Password must contain at least one digit."
        elif not any(char.isupper() for char in password):
            return "Password must contain at least one uppercase letter."
        elif not any(char.islower() for char in password):
            return "Password must contain at least one lowercase letter."
        elif not any(char in "!@#$%^&*()_+-=[]{};':\"\\|,.<>/?`~" for char in password):
            return "Password must contain at least one special character."
        else:
            return None
        


@bp.route('/registration',methods=['GET','POST'])
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
                return render_template('registration.html',error=error)
        return render_template('registration.html')
    

@bp.route('/registration/vehicle',methods=['GET','POST'])
def registration_vehicle():
    with current_app.app_context():
        error=None
        if request.method=='POST':
            return render_template('registration_vehicle.html')



@bp.route('/logout')
def logout():   
    session.clear()
    return redirect('login')