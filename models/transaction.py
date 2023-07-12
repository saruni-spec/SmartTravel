from extensions.extensions import db
from sqlalchemy import ForeignKey






class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(100),ForeignKey('user.user_name'),nullable=False)
    vehicle_id=db.Column(db.String(100),ForeignKey('vehicle.no_plate'),nullable=False)
    paid_at=db.Column(db.DateTime,nullable=False)
    booking_id=db.Column(db.Integer,ForeignKey('booking.id'),nullable=False)
    amount=db.Column(db.Integer,nullable=False)
    rating=db.Column(db.Integer,nullable=True,default=0)
    payment_type=db.Column(db.String(20),nullable=True)
    card_number=db.Column(db.String(20),nullable=True)
    status=db.Column(db.String(20),nullable=False,default="pending")


    

    def __init__(self,user_name,vehicle_id,paid_at,booking_id,amount,rating,payment_type,card_number):
        self.user_name=user_name
        self.vehicle_id=vehicle_id
        self.paid_at=paid_at
        self.booking_id=booking_id
        self.amount=amount
        self.rating=rating
        self.payment_type=payment_type
        self.card_number=card_number

    def complete_payment(self):
        self.status="completed"
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    

    