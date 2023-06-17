
from extensions.extensions import db,bcrypt

from sqlalchemy.orm import relationship
from .driver import Driver
from .owner import Owner
from .booking import Booking








class User(db.Model):
    __tablename__="user"
    user_name=db.Column(db.String(100),primary_key=True)
    email=db.Column(db.String(100),nullable=True)
    password=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(100),nullable=True)
    address=db.Column(db.String(100),nullable=True)

    driver_details = relationship("Driver", backref="user_is_driver", uselist=False )
    owner_details = relationship("Owner", backref="user_is_owner", uselist=False )
    booking_details = relationship("Booking", backref="booking" )

    def __init__(self,username):
        self.user_name=username

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.user_name
    
    def is_active(self):
        return True
    
    def check_if_driver(self):
        driver = Driver.query.filter_by(user_name=self.user_name).first()
        return True if driver is not None else False

    
    def check_if_owner(self):
        owner = Owner.query.filter_by(user_name=self.user_name).first()
        return True if owner is not None else False

    def save(self,password):
        self.password=bcrypt.generate_password_hash(password)
        self.is_driver=False
        self.is_owner=False
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



    def delete(self):
        db.session.delete(self)
        db.session.commit()
   