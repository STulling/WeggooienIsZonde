import hashlib
import json
from main import app
salt = app.config['SALT']

def hash_sha256(data: str) -> str:
    """
    Hashes a string with sha256 and salt
    """
    return hashlib.sha256((data + salt).encode()).hexdigest()