from flask import Blueprint, jsonify

def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    api = Blueprint('api', __name__, url_prefix='/api')

    from routes import item_blueprint
    api.register_blueprint(item_blueprint)

    from routes import admin_blueprint
    api.register_blueprint(admin_blueprint)

    app.register_blueprint(api)

    @app.errorhandler(404)
    def normal404(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def normal405(e):
        return jsonify({"error": "Method not allowed"}), 405