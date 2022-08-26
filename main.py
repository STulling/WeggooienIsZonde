from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api import register_blueprints
from json import load

app = Flask(__name__)
app.config["DEBUG"] = True

for key, value in load(open('config.json')).items():
    app.config[key] = value

db = SQLAlchemy(app)

if __name__=="__main__":
    register_blueprints(app)
    app.run()