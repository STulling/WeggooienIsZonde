import flask
from data import AuthorizeToken

def require_auth(func, role: str = None):
    """
    Decorator to require a certain role to access a route
    """
    def wrapper(*args, **kwargs):
        token = flask.request.headers.get('auth')
        user = AuthorizeToken(token)
        if user is None:
            return flask.jsonify({"error": "Invalid token"}), 401
        if role is not None and user.role != role:
            return flask.jsonify({"error": "Not authorized"}), 403
        return func(user, *args, **kwargs)
    return wrapper