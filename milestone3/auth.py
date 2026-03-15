import random
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Securely fetch secret key from .env
SECRET_KEY = os.getenv("JWT_SECRET", "default_secret_for_dev")

def generate_otp():
    """Generates a 6-digit random OTP."""
    return str(random.randint(100000, 999999))

def create_jwt(email):
    """Creates a JWT token valid for 1 hour."""
    payload = {
        "email": email,
        # Use timezone-aware UTC for expiration
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt(token):
    """Decodes and verifies the JWT token."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except Exception:
        # Returns None if token is expired or invalid
        return None

