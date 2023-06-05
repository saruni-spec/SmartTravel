import re
from email.utils import parseaddr

def validate_password(password):
        if len(password) < 12:
            return "Password must be at least 12 characters long."
        elif not any(char.isdigit() for char in password):
            return "Password must contain at least one digit."
        elif not any(char.isupper() for char in password):
            return "Password must contain at least one uppercase letter."
        elif not any(char.islower() for char in password):
            return "Password must contain at least one lowercase letter."
        elif not any(char in "!@#$%^&*()_+-=[]{};':\"\\|,.<>/?`~" for char in password):
            return "Password must contain at least one special character."
        else:
            return None

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    valid=re.match(pattern, email) is not None
    if valid:
    # Use email module to validate email format
        valid='@' in parseaddr(email)[1]
        if not valid:
            return "Invalid email format."
        else:
            return None
