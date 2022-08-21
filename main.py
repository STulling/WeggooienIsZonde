from flask import Blueprint, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from routes import item_blueprint

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://test.db'
db = SQLAlchemy(app)

api = Blueprint('api', __name__, url_prefix='/api')

@app.errorhandler(404)
def normal404(e):
    return jsonify({"error": "Not found"}), 404

api.register_blueprint(item_blueprint)
app.register_blueprint(api)

app.run()