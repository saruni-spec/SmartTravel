from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from extensions.extensions import *
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from views.registration import bp as  registration_bp
from views.login import bp as login_bp
from views.map  import bp as map_bp
from views.profile import bp as profile_bp
from views.payment import bp as payment_bp
from views.book import bp as book_bp

from models.user import User

app = Flask(__name__)

app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(map_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(book_bp)

app.config['SECRET_KEY']='mysecretkey'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAWYvsq4IwJAe-0p6kWv5pm20hj5BrIFvo"

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['MAIL_SERVER'] = 'smtp-relay.sendinblue.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'oddsthingshere@gmail.com'  
app.config['MAIL_PASSWORD'] = '2Eq6Gy87LKVfhzAv'  
app.config['MAIL_DEFAULT_SENDER'] = 'oddsthingshere@gmail.com'  
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://boss:boss%40mysql@localhost:3306/SmartTravel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

GoogleMaps(app)
bcrypt.init_app(app)
mail.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()

csrf = CSRFProtect()
csrf.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(username):
    # This callback is used by the login manager to load the current user.
    return User(username)


map_key='AIzaSyAWYvsq4IwJAe-0p6kWv5pm20hj5BrIFvo'

if __name__ == '__main__':
    app.run(debug=True)


