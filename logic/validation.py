import re
from email.utils import parseaddr
import random



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


def generate_verification_code():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = 6
    code = ''.join(random.choices(chars, k=length))
    return code


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    

def valid_number(phone_number):
    if not isinstance(phone_number, str):
        return False

    # Check if all characters are digits
    if not phone_number.isdigit():
        return False

    # Check if the length is exactly 10
    if len(phone_number) != 10:
        return False

    # Check if the first character is '0'
    if phone_number[0] != '0':
        return False

    return True

def valid_plate(s):
    if not isinstance(s, str):
        return False

    # Check if the length is exactly 7
    if len(s) != 7:
        return False

    # Check if the first 3 characters are letters
    if not s[:3].isalpha():
        return False

    # Check if the middle 3 characters are numbers
    if not s[3:6].isdigit():
        return False

    # Check if the last character is a letter
    if not s[-1].isalpha():
        return False

    return True
def valid_licence(phone_number):
    if not isinstance(phone_number, str):
        return False

    # Check if all characters are digits
    if not phone_number.isdigit():
        return False

    # Check if the length is exactly 10
    if len(phone_number) != 10:
        return False

    # Check if the first character is '0'
    

    return True