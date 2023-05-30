
from extensions.extensions import db,bcrypt



class User(db.Model):
    __tablename__="user"
    user_name=db.Column(db.String(100),primary_key=True)
    email=db.Column(db.String(100),nullable=True)
    password=db.Column(db.String(100),nullable=False)
    phone=db.Column(db.String(100),nullable=True)
    address=db.Column(db.String(100),nullable=True)
    is_driver=db.Column(db.Boolean,nullable=False)
    is_owner=db.Column(db.Boolean,nullable=False)

    def __init__(self,username):
        self.user_name=username

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.user_name
    
    def is_active(self):
        return True


    def save(self,password):
        self.password=bcrypt.generate_password_hash(password)
        self.is_driver=False
        self.is_owner=False
        db.session.add(self)
        db.session.commit()
        
    
    def status(self,status="is_active"):
        self.status=status
        return self.status

    def update_password(self,password):
        self.password=bcrypt.generate_password_hash(password)
        db.session.commit()

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def change_username(self,username):
        self.user_name=username
        db.session.commit()

    def add_email(self,email):
        self.email=email
        db.session.commit()

    def add_phone(self,phone):
        self.phone=phone
        db.session.commit()

    def add_address(self,address):
        self.address=address
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
   