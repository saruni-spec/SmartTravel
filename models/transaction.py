from extensions.extensions import db
from sqlalchemy import ForeignKey
from datetime import datetime





class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(100),ForeignKey('user.user_name'),nullable=False)
    vehicle_id=db.Column(db.String(100),ForeignKey('vehicle.no_plate'),nullable=False)
    paid_at=db.Column(db.String(50),nullable=False)
    time=db.Column(db.String(50))
    booking_id = db.Column(db.Integer, ForeignKey('booking.id'), unique=True, nullable=False)
    amount=db.Column(db.Integer,nullable=False)
    rating=db.Column(db.Integer,nullable=True,default=0)
    payment_type=db.Column(db.String(20),nullable=True)
    card_number=db.Column(db.String(20),nullable=True)
    phone=db.Column(db.String(50))
    status=db.Column(db.String(20),nullable=False,default="pending")


    

    def __init__(self,user_name,vehicle_id,booking_id,amount):
        self.user_name=user_name
        self.vehicle_id=vehicle_id
        self.paid_at=datetime.now().strftime("%Y-%m-%d")
        self.time=datetime.now().strftime("%H:%M:%S")
        self.booking_id=booking_id
        self.amount=amount
    
    def add_payment_type(self,payment_type,number):
        self.payment_type=payment_type
        if payment_type=="card":
            self.card_number=number
        else:
            self.phone=number
        db.session.commit()

    def complete_payment(self):
        self.status="completed"
        db.session.commit()
    
    def make_rating(self,rating):
        self.rating=rating
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def change_date(self):
        dt = datetime.strptime(self.paid_at, "%Y-%m-%d %H:%M:%S")
        new_date_string = dt.strftime("%Y-%m-%d")
        self.paid_at=new_date_string
        db.session.commit()
    

    