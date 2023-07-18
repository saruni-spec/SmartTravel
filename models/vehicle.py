from extensions.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .booking import Booking
from .transaction import Transaction

from datetime import datetime






class Vehicle(db.Model):
    __tablename__="vehicle"
   
    vehicle_type=db.Column(db.String(50))
    no_plate=db.Column(db.String(50),primary_key=True)
    capacity=db.Column(db.Integer)
    owner_username=db.Column(db.String(100),ForeignKey('owner.user_name'),nullable=False)
    driver_username=db.Column(db.String(100),ForeignKey('driver.user_name'),nullable=True)
    color=db.Column(db.String(50))
    is_active=db.Column(db.Boolean,default=False)
    verification_code=db.Column(db.String(50))
    for_hire=db.Column(db.Boolean,default=False)
    build_type=db.Column(db.String(50))
    date_registered=db.Column(db.String(50))

    balance=db.Column(db.Float,nullable=True)

    rating=db.Column(db.Float,nullable=True)

    hiring_cost=db.Column(db.Float,nullable=True)
    fare=db.Column(db.Float,nullable=True)

    booking_details = relationship("Booking", backref="bookings" )
    transactions=relationship("Transaction",backref="transactions")
   
    
    def __init__(self,no_plate):
        self.no_plate=no_plate

    def is_active(self):
        return self.is_active
        
    def get_id(self):
        return self.no_plate
    
    def add_driver(self,driver_username):
        self.driver_username=driver_username
        db.session.commit()
            
    def save(self,vehicle_type,owner,capacity,color,build_type):
        self.vehicle_type=vehicle_type
        self.owner_username=owner
        self.capacity=capacity
        self.color=color
        self.balance=0
        self.build_type=build_type
        self.date_registered=datetime.now().strftime("%Y-%m-%d")
        
        db.session.add(self)
        db.session.commit()

    def change_driver(self,driver):
        self.driver_username=driver
        db.session.commit()

    def change_owner(self,owner):
        self.owner_username=owner
        db.session.commit()

    def change_capacity(self,capacity):
        self.capacity=capacity
        db.session.commit()

    def change_color(self,color):   
        self.color=color
        db.session.commit()

    def unregister_vehicle(self):
        self.is_active=False
        db.session.commit()
        
        
    def allow_hiring(self):
        self.for_hire=True
        db.session.commit()

    def disallow_hiring(self):
        self.for_hire=False
        db.session.commit()

    def commit(self):
        db.session.commit() 

    def set_fare(self,fare):
        self.fare=fare
        db.session.commit()

    def set_hiring_cost(self,hiring_cost):
        self.hiring_cost=hiring_cost
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def add_verification_code(self,code):
        self.verification_code=code
        db.session.commit()

    def change_type(self,type):
        self.vehicle_type=type
        db.session.commit()

    def add_payment(self,amount):
        self.balance+=amount
        db.session.commit()

    def payout(self,amount):
        self.balance-=float(amount)
        db.session.commit()

    def make_rating(self):
        total_rating=0
        if len(self.transactions)==0:
            self.rating=0
        else:
            for rating in self.transactions:
                total_rating+=rating.rating
            average_rating=total_rating/len(self.transactions)
            self.rating=average_rating

    
        
