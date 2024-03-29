from flask import render_template,Blueprint,current_app,redirect,session,make_response
from flask import request
from models.user import User
from flask_login import login_user,current_user,logout_user,login_required
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError
from datetime import timedelta
from flask import url_for
from models.vehicle import Vehicle




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
                return error,404
            
            username=request.form.get('username')
            password=request.form.get('password')
            user = User.query.filter_by(user_name=username).first()
            if not user:
                user=User.query.filter_by(email=username).first()
                if not user:
                    error='Invalid User'
                    return render_template('login.html',error=error,username=username)
            
            
            if user and user.verify_password(password):
                login_user(user)
                session['current_user']=current_user.user_name
                if current_user.is_admin():
                    return redirect('/admin')
                else:
                    response = make_response(redirect(url_for('index.index')))
                    response.set_cookie('username', username, max_age=timedelta(days=1))
                    return response
            elif  user and not user.verify_password(password):
                error='Invaid Password'
                return render_template('login.html',error=error,username=username)
            else:
                error='Invalid User'
                return render_template('login.html',error=error,username=username)
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    with current_app.app_context():
        session.clear()
        logout_user()
        return redirect(url_for('index.index'))
    
  