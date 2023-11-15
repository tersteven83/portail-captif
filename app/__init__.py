from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import gammu
import hashlib, random


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        # SQLALCHEMY_DATABASE_URI='mysql+pymysql://user:user@localhost/portail-captif',
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://raduser:radpass@192.168.11.250/raddb',
        # SQLALCHEMY_ECHO=True,
        SECRET_KEY='dev'
    )
    db.init_app(app)

    from . import models
    with app.app_context():
        db.create_all()

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import user
    app.register_blueprint(user.bp)
    
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

def hash_password(password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    return sha1.hexdigest()

def verify_password(entered_passwd, stored_hashed_passwd):
    entered_passwd_hash = hash_password(entered_passwd)
    return entered_passwd_hash == stored_hashed_passwd

def generate_passcode():
    return random.randint(100000, 999999)

def is_valid_phone_number(phone_number):
    """Returns True if the phone number is valid, False otherwise."""

    # Vérifie que la chaîne de caractères commence par +

    if not phone_number.startswith("+"):
        return False

    # Vérifie que la chaîne de caractères contient 13 chiffres

    if len(phone_number) < 12:
        return False

    # Vérifie que la chaîne de caractères ne contient que des chiffres

    for char in phone_number[1:]:
        if not char.isdigit():
            return False

    return True


def is_number(value):
    return isinstance(value, (int, float))
