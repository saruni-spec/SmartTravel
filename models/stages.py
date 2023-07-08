from extensions.extensions import db
from models.routes import Route




class Stages(db.Model):
    __tablename__ = "stage"
    stage_no=db.Column(db.Integer,primary_key=True)
    latitude=db.Column(db.Float)
    longitude=db.Column(db.Float)
    stage_name=db.Column(db.String(100))
    stage_description=db.Column(db.String(100))
    


    def __init__(self,stage_no):
        self.stage_no=stage_no

    def save(self,latitude,longitude,stage_name,stage_description,route_no):
        self.latitude=latitude
        self.longitude=longitude
        self.stage_name=stage_name
        self.stage_description=stage_description

        db.session.add(self)
        db.session.commit()

    def change_stage_name(self,stage_name):
        self.stage_name=stage_name
        db.session.commit()
        


    
   