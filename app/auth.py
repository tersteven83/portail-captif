import requests
import jwt
from flask import (Blueprint, flash, redirect, g,
                   url_for, render_template, request, jsonify,
                   session)
from .models import *
from . import sendSMS, db
from sqlalchemy import text

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/number', methods=('GET', 'POST'))
def number():
    # Les vouchers disponibles
    voucher_dispo = Voucher.query.\
        filter(
            Voucher.is_active == False,
            Voucher.date == None,
            Voucher.telephone_number == None
        )
    # compter le nombre de voucher code dispo, si c'est inférieur ou égal à 100, on alerte l'admin
    num_admin = "+261333476904"
    nb_voucher = voucher_dispo.count()
    if nb_voucher in range(0, 100, 10):
        sendSMS(f"Bonjour admin, vous devriez ajouter de nouvels code voucher, il n'y en reste plus que {nb_voucher}",
                num_admin)

    if request.method == "POST":
        telephone_number = request.form.get('telephoneNumber')

        # vérifier si le numero de telephone est valide
        if is_valid_phone_number(telephone_number):
            # fetch the first non active voucher code
            voucher_code = voucher_dispo.first()
            print(voucher_code)
            if voucher_code is not None:
                # vérifier si le voucher_code a un attribut "*-Password"
                voucher_attr_check = Radcheck.query.filter(Radcheck.username == voucher_code.voucher_code)
                passwd = None
                for row in voucher_attr_check:
                    if "-Password" in row.attribute:
                        passwd = row.value
                        break
                
                if passwd:
                    msg = f"Voici votre code d'identification \
                        username: {voucher_code.voucher_code} \
                        password: {passwd}"
                else:
                    msg = f"Voici votre code d'identification \
                        username: {voucher_code.voucher_code} \
                        password: -"
                
                if sendSMS(msg, telephone_number):
                    print("OK!!")
                    # Message envoyé avec succès
                    success = "Le code est envoyé avec succès, vérifiez votre téléphone"
                    flash(success)
                    
                    # mettre à jour le voucher envoyé, marqué comme actif
                    Voucher.query.filter(Voucher.id == voucher_code.id).update({
                        Voucher.date: datetime.now(),
                        Voucher.telephone_number: telephone_number
                    })
                    db.session.commit()
                    return redirect("http://192.168.10.1:8002/index.php?zone=ambohijatovo")
                else:
                    print("Le forfait est épuisé")
        else:
            print("Misy tsy mety")

    return render_template('auth/number.html')


def is_valid_phone_number(phone_number):
    """Returns True if the phone number is valid, False otherwise."""

    # Vérifie que la chaîne de caractères commence par 00

    if not phone_number.startswith("00"):
        return False

    # Vérifie que la chaîne de caractères contient 13 chiffres

    if len(phone_number) < 13:
        return False

    # Vérifie que la chaîne de caractères ne contient que des chiffres

    for char in phone_number[2:]:
        if not char.isdigit():
            return False

    return True


@bp.route('/hello', methods=['GET'])
def hello():
    verification, decoded_message = verifier_token()
    if verification:
        session['user_id'] = decoded_message['user_id']
        print(decoded_message)
        return jsonify({'message': 'Accès autorisé'})
    else:
        return jsonify({'message': 'Accès non autorisé'}), 401

def verifier_token():
    token = request.headers.get('Authorization')
    if not token:
        return False, {"error": "Token manquant"}
    
    try:
        # Extrait le token du format 'Bearer <token>'
        token = token.split()[1]
        decoded_token = jwt.decode(token, 'steven', algorithms=['HS256'])
        return True, decoded_token
    except jwt.ExpiredSignatureError:
        return False, {"error": "Erreur de signature"}
    except jwt.InvalidTokenError:
        return False, {"error": "Token invalide"}

@bp.route('/test')
def test():
    print(session.get("user_id"))
    return "hello"