from flask import render_template,Blueprint,redirect,session
from flask import url_for
from flask_login import current_user,login_required
from models.user import User
from models.driver import Driver






bp=Blueprint('index',__name__)

@bp.route('/')
def index():  
   
    if current_user.is_authenticated:
        user=User.query.filter_by(user_name=current_user.user_name).first()
            
            
        if user.is_admin():
            
            return redirect(url_for('admin.admin'))
        else:
            if user.driver_details and user.owner_details:
                return redirect(url_for('index.driver'))
            elif user.driver_details and not user.owner_details:
                return redirect(url_for('index.driver'))
            elif not user.driver_details and user.owner_details:
                return redirect(url_for('index.owner'))
            else:

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

@bp.route('/driver')
def driver():
    return render_template('driver.html')

@bp.route('/owner')
def owner():

    return render_template('owner.html')

@bp.route('/about')
def about():
    return render_template('about.html')