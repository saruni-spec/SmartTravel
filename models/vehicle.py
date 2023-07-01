from extensions.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .booking import Booking




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

    booking_details = relationship("Booking", backref="bookings" )
    
    def __init__(self,no_plate):
        self.no_plate=no_plate

    def is_active(self):
        return self.is_active
        
    def get_id(self):
        return self.no_plate
    
    def add_driver(self,driver_username):
        self.driver_username=driver_username
        db.session.commit()
        
    def save(self,vehicle_type,owner,driver,capacity,color,verification_code):
        self.vehicle_type=vehicle_type
        self.owner_username=owner
        self.driver_username=driver
        self.capacity=capacity
        self.color=color
        self.verification_code=verification_code
        
        db.session.add(self)
        db.session.commit()

    def change_driver(self,driver_contact):
        self.driver_email=driver_contact
        db.session.commit()

    def change_owner(self,owner_contact):
        self.owner_email=owner_contact
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
        
    
    def accept_bookings(self,no_of_seats):
        if self.temporary_capacity>0:
            if self.temporary_capacity>=no_of_seats:
                self.temporary_capacity=self.temporary_capacity-no_of_seats
                return True
    
    def check_availability(self):
        return self.temporary_capacity
    
    def stop_bookings(self):
        from flask import session
        self.temporary_capacity=self.capacity
        session['docked']=False
        
        

        