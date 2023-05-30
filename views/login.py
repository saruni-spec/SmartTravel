from flask import render_template,Blueprint,current_app,redirect
from flask import request
from models.user import User
from flask import url_for
from flask_login import login_user
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError

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
                return redirect(url_for('map.mapview2'))
            elif  user and not user.verify_password(password):
                error='Invaid Password'
                return render_template('login.html',error)
            else:
                error='Invalid User'
                return render_template('login.html',error)
    return render_template('login.html')