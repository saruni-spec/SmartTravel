import random
import string

# Password validation function
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

# Generate random password
def generate_random_password():
    length = 12
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{};':\"\\|,.<>/?`~"
    return ''.join(random.choice(chars) for _ in range(length))

# Sample user data
sample_user_data = [
    {
        "user_name": "user1",
        "email": "user1@example.com",
        "password": generate_random_password(),
        "phone": "123456789",
        "address": "Address 1"
    },
    {
        "user_name": "user2",
        "email": "user2@example.com",
        "password": generate_random_password(),
        "phone": "987654321",
        "address": "Address 2"
    },
    # Add more user entries here
    # ...
]

# Create 20 user records
users = []

for i in range(20):
    password = generate_random_password()
    while error := validate_password(password):
        password = generate_random_password()
    
    user_data = {
        "user_name": f"user{i+1}",
        "email": f"user{i+1}@example.com",
        "password": password,
        "phone": "123456789",
        "address": f"Address {i+1}"
    }
    users.append(user_data)

no='HIJ234'
print(no=='HIJ234')