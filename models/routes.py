from extensions.extensions import db

class Route(db.Model):
    __tablename__ = 'route'
    route_id = db.Column(db.Integer, primary_key=True)
    route_start=db.Column(db.String(50))
    route_end=db.Column(db.String(50))
    route_distance=db.Column(db.Integer)
    
    stages = db.relationship("Stages", backref="route")
    
    def __init__(self,route_id):
        self.route_id = route_id
    
    def is_viable(self,is_viable=True):
        self.is_viable = is_viable

    def save(self,route_start,route_end,route_distance):
        self.route_start = route_start
        self.route_end = route_end
        self.route_distance = route_distance
    
    
        db.session.add(self)
        db.session.commit()

    def update(self,route_start,route_end,route_distance):
        self.route_start = route_start
        self.route_end = route_end
        self.route_distance = route_distance
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


