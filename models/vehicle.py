from extensions.extensions import db

class Vehicle(db.Model):
    __tablename__='vehicle'
    vehicle_type=db.Column(db.String(50))
    no_plate=db.Column(db.String(50),primary_key=True)
    capacity=db.Column(db.Integer)
    owner=db.Column(db.String(50))
    owner_email=db.Column(db.String,db.ForeignKey("user.email"),nullable=False)
    driver_email=db.Column(db.String,db.ForeignKey("user.email"),nullable=False)

    driver=db.relationship("User",foreign_keys=[driver_email],backref="driver",lazy=True)
    owner=db.relationship("User",foreign_keys=[owner_email],backref="owner",lazy=True)

    def __init__(self,no_plate):
        self.id=no_plate

    def is_active(self):
        return True
    
    def get_id(self):
        return self.no_plate
    
    def save(self,vehicle_type,driver_name,driver_contact,capacity):
        self.vehicle_type=vehicle_type
        self.driver_name=driver_name
        self.driver_contact=driver_contact
        self.capacity=capacity
        db.session.add(self)
        db.session.commit()

    def update(self,driver_name,driver_contact):
        self.driver_name=driver_name
        self.driver_contact=driver_contact
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    