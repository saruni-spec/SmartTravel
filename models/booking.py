from extensions.extensions import db
from sqlalchemy import ForeignKey



class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(100),ForeignKey("user.user_name"),nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    pickup_point = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    vehicle_plate=db.Column(db.String(50),ForeignKey("vehicle.no_plate"),nullable=False)
    Fare=db.Column(db.Integer, nullable=False)
    Status=db.Column(db.String(100), nullable=False)
    payment_type=db.Column(db.String(20),nullable=False)
    card_number=db.Column(db.String(20),nullable=False)


    def __init__(self, user_email, phone, date, time, pickup_point, destination, vehicle, Fare):
        self.email = user_email
        self.phone = phone
        self.date = date
        self.time = time
        self.pickup_point = pickup_point
        self.destination = destination
        self.vehicle = vehicle
        self.Fare = Fare
        self.Status = "Pending"

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def payment(self, payment_type, card_number):
        self.payment_type = payment_type
        self.card_number = card_number
        self.Status="Paid"
        db.session.add(self.payment_type,self.card_number,self.Status)
        db.session.commit()

    def cancel(self):
        self.Status="Cancelled"
        db.session.add(self.Status)
        db.session.commit()
        
    
    

    
        