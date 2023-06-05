from extensions.extensions import db

class Vehicle(db.Model):
    __tablename__='vehicle'
    vehicle_type=db.Column(db.String(50))
    no_plate=db.Column(db.String(50),primary_key=True)
    capacity=db.Column(db.Integer)
    owner_email=db.Column(db.String,nullable=False)
    driver_email=db.Column(db.String,nullable=False)
    color=db.Column(db.String(50))
    is_active=db.Column(db.Boolean,default=True)

    driver=db.relationship("User",foreign_keys=[driver_email],backref="driver",lazy=True)
    owner=db.relationship("User",foreign_keys=[owner_email],backref="owner",lazy=True)

    def __init__(self,no_plate):
        self.id=no_plate

    def is_active(self):
        return self.is_active
        
    def get_id(self):
        return self.no_plate
    
    def save(self,vehicle_type,owner,driver,capacity,color):
        self.vehicle_type=vehicle_type
        self.owner=owner
        self.driver=driver
        self.capacity=capacity
        self.color=color
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