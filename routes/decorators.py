import flask
from functools import wraps
from data import AuthorizeToken

def require_auth(func, role: str = "user"):
    """
    Decorator to require a certain role to access a route
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = flask.request.headers.get('auth')
        user = AuthorizeToken(token)
        if user is None:
            return flask.jsonify({"error": "Invalid token"}), 401
        if role is not None and user.role != role:
            return flask.jsonify({"error": "Not authorized"}), 403
        return func(user, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def require_admin(func):
    """
    Decorator to require an admin role to access a route
    """
    return require_auth(func, role="admin")