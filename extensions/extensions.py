# extensions.py
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import os

bcrypt = Bcrypt()
mail = Mail()
db = SQLAlchemy()

from intasend import APIService

token = os.environ.get("intasend_test_api_key")
publishable_key = os.environ.get("intasend_test_publishable_key")
service = APIService(token=token, publishable_key=publishable_key, test=True)
