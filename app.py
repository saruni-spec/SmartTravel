from flask import Flask, session,flash,redirect
from flask_googlemaps import GoogleMaps
from extensions.extensions import *
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate



from views.index import bp as index_bp
from views.registration import bp as  registration_bp
from views.login import bp as login_bp
from views.map  import bp as map_bp
from views.profile import bp as profile_bp
from views.payment import bp as payment_bp
from views.booking import bp as booking_bp
from views.reg_stages import bp as reg_stages_bp
from extensions.tasks import bp as tracking_bp
from views.admin import bp as admin_bp









from models.user import User
from flask import request

app = Flask(__name__)

app.register_blueprint(registration_bp)
app.register_blueprint(login_bp)
app.register_blueprint(map_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(index_bp)
app.register_blueprint(reg_stages_bp)
app.register_blueprint(tracking_bp)
app.register_blueprint(admin_bp)


app.config['SECRET_KEY']='mysecretkey'
app.config['GOOGLEMAPS_KEY'] = 'AIzaSyA_JxBRmUKjcpPLWXwAagTX9k19tIWi2SQ'

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
migrate = Migrate(app, db)


csrf = CSRFProtect()
csrf.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login.login'

@login_manager.user_loader
def load_user(username):
    # This callback is used by the login manager to load the current user.
    return User(username)

@app.before_request
def store_next_url():
    if request.endpoint != 'login.login' and request.endpoint != 'static' and request.path != '/favicon.ico':
        session['next_url'] = request.url

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to log out.')
    return redirect('/login')




@app.route('/')
def index():
    return redirect('/index')

@app.route('/favicon.ico')
def favicon():
    return '', 204



if __name__ == '__main__':
    app.run(debug=True)
    
    

