from flask import render_template,Blueprint,current_app,redirect,session,make_response
from flask import request
from models.user import User
from flask_login import login_user
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from datetime import timedelta

bp=Blueprint('login',__name__)

@bp.route('/login',methods=['GET','POST'])
def login():
    with current_app.app_context():
        error=None
        if request.method=='POST':
            token = request.form.get('csrf_token')
            try:
                validate_csrf(token)
            except ValidationError :
                error="Invalid CSRF token"
            
            username=request.form.get('username')
            password=request.form.get('password')
            user = User.query.filter_by(user_name=username).first()
            print(user,'user here')
            
            if user and user.verify_password(password):
                login_user(user)
                session['user_id']=user.get_id()
                session['email']=user.email
                session['phone']=user.phone
                session['address']=user.address
                next_url = session.get('next_url', '/profile')
                print(next_url,'next url')
                response = make_response(redirect(next_url))
                response.set_cookie('username', username, max_age=timedelta(days=1))
                return response
            elif  user and not user.verify_password(password):
                error='Invaid Password'
                return render_template('login.html',error)
            else:
                error='Invalid User'
                return render_template('login.html',error)
    return render_template('login.html')