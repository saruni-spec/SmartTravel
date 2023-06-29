from extensions.extensions import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


route_stage_table = Table(
    'route_stage',
    db.Model.metadata,
    Column('route_id', Integer, ForeignKey('route.id')),
    Column('stage_no', Integer, ForeignKey('stage.stage_no'))
)

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
        

class Route(db.Model):
    __tablename__ = 'route'
    id = db.Column(db.Integer, primary_key=True)
    route_distane=db.Column(db.Float)

    stages = relationship('Stages', secondary=route_stage_table, backref='routes')


    def __init__(self, stages):
        self.stages = stages

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def add_stage(self,stage_name):
        self.stage=stage_name
        self.save()