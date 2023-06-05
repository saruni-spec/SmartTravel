from extensions.extensions import db
from sqlalchemy import ForeignKey

class Stages(db.Model):
    __tablename__ = "stage"
    stage_no=db.Column(db.Integer,primary_key=True)
    latitude=db.Column(db.Float)
    longitude=db.Column(db.Float)
    stage_name=db.Column(db.String(100))
    stage_description=db.Column(db.String(100))
    route_id=db.Column(db.Integer)

    route_id = db.Column(db.Integer, ForeignKey('route.route_id'))

    def __init__(self,stage_no):
        self.stage_no=stage_no

    def save(self,latitude,longitude,stage_name,stage_description,route_no):
        self.latitude=latitude
        self.longitude=longitude
        self.stage_name=stage_name
        self.stage_description=stage_description
        self.route_no=route_no
        db.session.add(self)
        db.session.commit()

    def change_stage_name(self,stage_name):
        self.stage_name=stage_name
        db.session.commit()
        