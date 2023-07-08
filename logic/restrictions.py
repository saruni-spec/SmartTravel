from functools import wraps
from models.owner import Owner
from models.driver import Driver
from flask_login import current_user


def is_driver(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            driver = Driver.query.filter_by(user_name=current_user.user_name).first()
            if not driver:
                # Redirect or return an error message if user is not a driver
                return "Unauthorized: Access denied for non-drivers"
            return func(*args, **kwargs)
        return wrapper

def is_owner(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        owner = Owner.query.filter_by(user_name=current_user.user_name).first()
        if not owner:
            # Redirect or return an error message if user is not an owner
            return "Unauthorized: Access denied for non owners"
        return func(*args, **kwargs)
    return wrapper
