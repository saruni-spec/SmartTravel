
from extensions.extensions import db,bcrypt

from sqlalchemy.orm import relationship
from .driver import Driver
from .owner import Owner
from .booking import Booking
from .transaction import Transaction


from datetime import datetime
from flask_login import current_user












class User(db.Model):
    __tablename__="user"
    user_name=db.Column(db.String(100),primary_key=True)
    first_name=db.Column(db.String(100),nullable=False)
    other_name=db.Column(db.String(100),nullable=True)
    email=db.Column(db.String(100),nullable=True)
    password=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(100),nullable=True)
    address=db.Column(db.String(100),nullable=True)
    role=db.Column(db.String(50))
    date_registered=db.Column(db.String(50))
    card_number=db.Column(db.String(100))

    driver_details = relationship("Driver", backref="user_is_driver", uselist=False )
    owner_details = relationship("Owner", backref="user_is_owner", uselist=False )
    booking_details = relationship("Booking", backref="booking" )
    transaction_details = relationship("Transaction", backref="transaction" )
    

    def __init__(self,username):
        self.user_name=username

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.user_name
    
    def is_active(self):
        return True
    
    def check_if_driver(self):
        
        user=User.query.filter_by(user_name=current_user.user_name).first()
        driver=user.driver_details
        
        if driver is None:
            return False
        else:
            return True

    
    def check_if_owner(self):
        user=User.query.filter_by(user_name=current_user.user_name).first()
        owner=user.owner_details
        print(owner,'owner')
        if owner is not None :
            return True
        else:
            return False

    def save(self,password,first_name,other_name,email):
        self.first_name=first_name
        self.other_name=other_name
        self.email=email
        self.role="user"
        
        self.password=bcrypt.generate_password_hash(password)
        self.date_registered=datetime.now().strftime("%Y-%m-%d")
        db.session.add(self)
        db.session.commit()
        
    
    def status(self,status="is_active"):
        self.status=status
        return self.status

    def update_password(self,password):
        self.password=bcrypt.generate_password_hash(password)
        db.session.commit()

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def change_user_name(self,username):
        self.user_name=username
        db.session.commit()

    def add_email(self,email):
        self.email=email
        db.session.commit()

    def add_phone(self,phone):
        self.phone=phone
        db.session.commit()

    def add_address(self,address):
        self.address=address
        db.session.commit()

    def add_card_number(self,card_number):
        self.card_number=card_number
        db.session.commit()

    def make_admin(self):
        self.role="admin"
        db.session.commit()

    def is_admin(self):
        return self.role=="admin"

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def commit(self):
        db.session.commit()

    def make_driver(self):
        self.role="driver"
        db.session.commit()
    
    def make_owner(self):
        self.role="owner"
        db.session.commit()

    def make_user(self):
        self.role="user"
        db.session.commit()