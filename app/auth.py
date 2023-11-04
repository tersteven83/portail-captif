import requests
from flask import (Blueprint, flash, redirect, g,
                   url_for, render_template, request)
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
            if voucher_code is not None:
                if sendSMS(voucher_code.voucher_code, telephone_number):
                    print("OK!!")
                    # Message envoyé avec succès
                    success = "Le code est envoyé avec succès, vérifiez votre téléphone"
                    flash(success)
                    
                    # mettre à jour le voucher envoyé, marqué comme actif
                    Voucher.query.filter(Voucher.id == voucher_code.id).update({
                        Voucher.is_active: True,
                        Voucher.date: datetime.now(),
                        Voucher.telephone_number: telephone_number
                    })
                    db.session.commit()
                    return redirect("http://192.168.11.1:8002/index.php?zone=serveur")
                else:
                    print("Le forfait est épuisé")
        else:
            print("Misy tsy mety")

    return render_template('auth/number.html')

@bp.route('/hello')
def hello():
    return 'Hello, World!'



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
