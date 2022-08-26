from base64 import b64decode
from main import db

# an example mapping using the base
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    role = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    appartment = db.Column(db.String, nullable=False)

def AuthorizeToken(token: str) -> User:
    """
    Authorizes a base 64 token
    """
    token = b64decode(token)
    token = token.split(b':')
    username = token[0].decode('utf-8')
    password = token[1].decode('utf-8')

    user = User.query.filter_by(username=username, password=password).first()
    return user