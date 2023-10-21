from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import gammu


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

def sendSMS(text, phone_number, config_file=None):
    """
    Send the voucher code to a phone number
    """

    # Create object for talking with phone
    state_machine = gammu.StateMachine()

    # load the config file
    if config_file is None:
    # ./gammurc
        state_machine.ReadConfig()
    else:
        state_machine.ReadConfig(Filename=config_file)

    # Connect to the phone
    state_machine.Init()

    # Prepare message data
    # We tell that we want to use first SMSC number stored in phone
    message = {
        "Text": text,
        "SMSC": {"Location": 1},
        "Number": phone_number,
    }
    try:
        # Actually send the message
        state_machine.SendSMS(message)
        return True
    except gammu.ERR_UNKNOWN:
        return False
