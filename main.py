from flask import Blueprint, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from api import register_blueprints

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

register_blueprints(app)

if __name__=="__main__":
    app.run()