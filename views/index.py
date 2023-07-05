from flask import render_template,Blueprint,redirect
from flask import url_for
from flask_login import current_user,login_required

bp=Blueprint('index',__name__)

@bp.route('/')
def index():  
    if current_user.is_authenticated:
        return redirect(url_for('index.home'))  
    else:
        return redirect(url_for('index.index_page'))
    
@bp.route('/home')
@login_required
def home():
    return render_template('home.html')

@bp.route('/index')
def index_page():
    return render_template('index.html')