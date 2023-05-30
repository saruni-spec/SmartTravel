# extensions.py
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
mail = Mail()
db = SQLAlchemy()