from flask import render_template,session,current_app,Blueprint,redirect,url_for
from flask import url_for
from flask import request
from email_validator import validate_email, EmailNotValidError
import random

bp=Blueprint('verification',__name__)

def validate_email(email):
    try:
        valid = validate_email(email)
        email = valid.email
        return None
    except EmailNotValidError:
        error = "Invalid email address"
        return error

def generate_verification_code():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = 6
    code = ''.join(random.choices(chars, k=length))
    return code


@bp.route('/verification',methods=['GET','POST'])
def verification():
    code=session.get('confirmation_code', None)
    error=None
    if request.method=='POST':
        if code==request.form['code']:
            return redirect(url_for('login'))
        else:
            error='Invalid code'
    return render_template('verification.html')