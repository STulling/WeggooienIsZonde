from flask import Blueprint
from data import User
from routes.decorators import require_admin

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.route('/debug', methods=['POST'])
@require_admin
def admin_debug(user: User):
    return "Success", 200
