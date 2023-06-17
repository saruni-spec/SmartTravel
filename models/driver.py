from extensions.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.vehicle import Vehicle



class Driver(db.Model):
    __tablename__ = 'driver'
    user_name=db.Column(db.String(100),ForeignKey('user.user_name'),nullable=False)
    licence_no=db.Column(db.String(100),primary_key=True)
    is_active=db.Column(db.Boolean,default=True)
    drives = relationship("Vehicle", backref="drives", uselist=False )
    
    

    def __init__(self,username,licence_no):
        self.user_name=username
        self.licence_no=licence_no

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.licence_no
    
    def is_active(self):
        return self.is_active
        
    def status(self,is_active):
        self.is_active=is_active
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    

    
    
   