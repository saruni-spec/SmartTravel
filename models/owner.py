from extensions.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.vehicle import Vehicle




class Owner(db.Model):
    __tablename__ = 'owner'
    user_name=db.Column(db.String(100),ForeignKey('user.user_name'),nullable=False)
    licence_no=db.Column(db.String(100),primary_key=True)

    vehicle_details = relationship("Vehicle", backref="owns",uselist=False )
    

    

    def __init__(self,username,licence_no):
        self.user_name=username
        self.licence_no=licence_no

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.licence_no
    
    def is_active(self):
        return True
        
    def status(self,status="is_active"):
        self.status=status
        return self.status
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    
   