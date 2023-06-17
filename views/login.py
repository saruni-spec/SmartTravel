from flask import render_template,Blueprint,current_app,redirect,session,make_response
from flask import request
from models.user import User
from flask_login import login_user
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from datetime import timedelta
from flask import url_for


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
                if user.check_if_driver() is True and user.check_if_owner() is True:
                    print(user.check_if_driver(),user.check_if_owner(),'both')
                    next_url = session.get('next_url', url_for('profile.profile_owner'))
                elif user.check_if_driver() is True:
                    print(user.check_if_driver(),'driver')
                    next_url = session.get('next_url', url_for('profile.profile_driver'))
                elif user.check_if_owner() is True:
                    print(user.check_if_owner(),'owner')
                    
                    next_url = session.get('next_url', url_for('profile.profile_owner'))
                else:
                    print('only user')
                    next_url = session.get('next_url', url_for('profile.rider'))
                
                if next_url == url_for('login.login'):
                    next_url = url_for('index.index')
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