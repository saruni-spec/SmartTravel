from extensions.extensions import db

class Notification():
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_sent = db.Column(db.DateTime)
    pickup_point = db.Column(db.String(200))
    destination = db.Column(db.String(200)) 

    def __init__(self, receiver_id, sender_id, time_sent, pickup_point, destination):
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.time_sent = time_sent
        self.pickup_point = pickup_point
        self.destination = destination

    def save(self):
        db.session.add(self)
        db.session.commit()
        