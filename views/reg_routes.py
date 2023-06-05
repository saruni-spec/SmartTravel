from flask import render_template,Blueprint
from flask import request
from models.routes import Route
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError

bp=Blueprint('routes',__name__)

@bp.route('/routes/registration',methods=['GET','POST'])
def route_registration():
    error=None
    if request.method=='POST':
        token=request.form.get('csrf_token')
        print('registering driver')
        try:
            validate_csrf(token)
        except ValidationError:
            error="Invalid CSRF token"
        route_id=request.form.get('route_no')
        route_start=request.form.get('route_start')
        route_end=request.form.get('route_end')
        route_distance=request.form.get('route_distance')
        route=Route(route_id)
        route.save(route_start,route_end,route_distance)
        
    return render_template('reg_routes.html')