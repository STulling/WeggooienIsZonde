from base64 import b64decode
from main import db
from utils import hash_sha256

# an example mapping using the base
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    role = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    appartment = db.Column(db.String, nullable=False)

def AuthorizeToken(token: str) -> User:
    """
    Authorizes a base 64 token in the format -> username:password

    :param token: the token to authorize
    :return: the user if the token is valid, None otherwise
    """
    if token is None:
        return None
    token = b64decode(token)
    token = token.split(b':')
    if len(token) != 2:
        return None
    username = token[0].decode('utf-8')
    password = token[1].decode('utf-8')
    # hash with sha256
    hashed_password = hash_sha256(password)
    del password

    user = User.query.filter_by(username=username, password=hashed_password).first()
    return user