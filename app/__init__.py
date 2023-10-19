from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://user:user@localhost/portail-captif',
        SQLALCHEMY_ECHO=True,
        SECRET_KEY='dev'
    )
    db.init_app(app)

    from . import models
    with app.app_context():
        db.create_all()

    from . import auth
    app.register_blueprint(auth.bp)

    return app
