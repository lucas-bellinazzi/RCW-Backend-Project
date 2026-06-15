from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config.settings import DATABASE_URI

db = SQLAlchemy()
ma = Marshmallow()

def configure_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)
