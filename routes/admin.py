from flask import Blueprint, jsonify, request
from data import Item, AuthorizeToken, Tag, User
import flask
from main import db
from routes.decorators import require_auth

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.route('/debug', methods=['POST'])
@require_auth(role="admin")
def admin_debug(user: User):
    return "Success", 200
