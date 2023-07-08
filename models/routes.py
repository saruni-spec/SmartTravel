from extensions.extensions import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship



route_stage_table = Table(
    'route_stage',
    db.Model.metadata,
    Column('route_id', Integer, ForeignKey('route.id')),
    Column('stage_no', Integer, ForeignKey('stage.stage_no'))
)

class Route(db.Model):
    __tablename__ = 'route'
    id = db.Column(db.Integer, primary_key=True)
    route_distane=db.Column(db.Float)

    stages = relationship('Stages', secondary=route_stage_table, backref='routes')

    def __init__(self, id):
        self.id = id
        
        

    def save(self):
        db.session.add(self)
        db.session.commit()

    def distane(self,distance):
        self.route_distane = distance
        db.session.commit()

    def stage(self,stages):
        self.stages = stages
        db.session.commit()




