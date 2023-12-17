from flask import (Blueprint, flash, redirect,
                   url_for, render_template, request)
from .models import *
from . import sendSMS, db, is_valid_phone_number, generate_passcode
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/number/<confirm_code>', methods=('GET', 'POST'))
def number(confirm_code):
    """
    Vérifier si le code est valide
    Demander le numéro téléphone de l'invité et lui envoyé un Voucher Code par SMS
    """
    if is_valid(confirm_code):
        # Les vouchers disponibles
        voucher_dispo = Voucher.query.\
            filter(
                Voucher.is_active == False,
                Voucher.date == None,
                Voucher.telephone_number == None,
                Voucher.mac_address == None,
                Voucher.printed == False
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
                    
                    # if sendSMS(msg, telephone_number):
                    if 1:
                        print("OK!!")
                        # Message envoyé avec succès
                        success = "Le code est envoyé avec succès, vérifiez votre téléphone"
                        flash(success)
                        
                        # mettre à jour le voucher envoyé, marqué comme actif
                        Voucher.query.filter(Voucher.id == voucher_code.id).update({
                            Voucher.date: datetime.now(),
                            Voucher.telephone_number: telephone_number
                        })
                        
                        Number_auth.query.filter(Number_auth.code == confirm_code).update({
                            Number_auth.already_ask_voucher: True                            
                        })
                        db.session.commit()
                        return redirect("http://192.168.110.1:8002/index.php?zone=ambohijatovo")
                    else:
                        print("Le forfait est épuisé")
            else:
                flash("Vérifié votre saisi l'ami", category='error')

        return render_template('auth/number.html')
    else:
        return '404 error not found', 404

@bp.route('/gather_id', methods=['GET', 'POST'])
def gather_id():
    """
    En cas d'oublie de mot de passe, l'utilisateur sera prié d'entrer son Identifiant(username)
    ou bien son numéro de téléphone afin de l'identifier dans la base de donnée.
    """
    if request.method == "POST":
        value = request.form.get("value")
        if is_valid_phone_number(value):
            # la valeur reçu du formulaire est un numéro de téléphone
            # vérifier sa présence dans la BD
            # si le numéro est present dans plus de 1 ligne, on affiche d'abord une page avec un bouton ok
            # si non on retourne son ID tout de suite dans user.edit_pwd
            try:
                user_info = Userinfo.query.filter(Userinfo.workphone == value).scalar()
                if user_info:
                    # générer un passcode et enregistrer dans la table userinfo
                    tmp_passcode = str(generate_passcode())
                    user_info.tmp_passcode = tmp_passcode

                    # Envoyer le passcode à l'utilisateur
                    msg = f"Votre pass code de réinitialisation de mot de passe : {tmp_passcode}"
                    # if sendSMS(msg, value):
                    if 1:
                        print('ok')
                        
                        # make the user_info editable
                        user_info.can_be_edited = True
                        db.session.commit()
                        return redirect(url_for('user.forgot_pwd', user_id=user_info.id))
                    else:
                        print("le code n'est pas envoyé")
                else:
                    flash("L'utilisatuer que vous cherchez n'existe pas", category='error')
            except MultipleResultsFound:
                user_infos = Userinfo.query.filter(Userinfo.workphone == value).all()
                # recupérer tous les id et les usernames
                # make all user_info editable
                user_ids = []
                usernames = []
                tmp_passcode = str(generate_passcode())
                for user_info in user_infos:
                    user_ids.append(user_info.id)
                    usernames.append(user_info.username)
                    user_info.can_be_edited = True
                    user_info.tmp_passcode = tmp_passcode
                
                # Envoyer le passcode à l'utilisateur
                msg = f"Votre pass code de réinitialisation de mot de passe : {tmp_passcode}"
                # if sendSMS(msg, value):
                if 1:
                    db.session.commit()
                    return render_template('user/choose_to_edit.html', user_ids=user_ids, usernames=usernames)
                else:
                    print("le code n'est pas envoyé")
                
        
        elif bool(re.match("^(?=.*[a-zA-Z])[a-zA-Z0-9_]+$", value)):
            # de la forme username
            username = value
            
            # vérifier si cet utilisateur a un work phone
            # si oui on envoi le passcode
            # sinon on demande son workphone
            
            user_info = Userinfo.query.filter(Userinfo.username == username).one_or_none()
            if user_info:
                
                # make the user_info editable
                user_info.can_be_edited = True
                if user_info.workphone:
                    wk_phone = user_info.workphone
                    tmp_passcode = str(generate_passcode())
                    user_info.tmp_passcode = tmp_passcode

                    # Envoyer le passcode à l'utilisateur
                    msg = f"Votre pass code de réinitialisation de mot de passe : {tmp_passcode}"
                    # if sendSMS(msg, wk_phone):
                    if 1:
                        print(msg + " work-phone: " + user_info.workphone)
                        db.session.commit()
                        return redirect(url_for('user.forgot_pwd', user_id=user_info.id))
                    else:
                        print("le code n'est pas envoyé")
                else:
                    # l'utilisateur n'a pas de numéro téléphone
                    flash("Vous n'avez pas encore de numéro de téléphone de travail, veuillez me renseignez")
                    db.session.commit()
                    return redirect(url_for('user.add_work_phone', ID=user_info.id, is_session=0))
                
            else:
                flash("L'utilisateur que vous cherchez n'existe pas", category='error')
        else:
            flash("Veuillez vérifier votre saisi", category='error')
            
    return render_template('auth/gather_id.html')

def is_valid(confirm_code):
    """
    Vérifier la validation du code dans la table number_auth, si sa date d'expiration n'est pas encore dépassé
    """
    try:
        code = Number_auth.query.filter(Number_auth.code == confirm_code).one()
        if datetime.now() < code.expiration and not code.already_ask_voucher:
            return True
        else:
            return False
            
    except NoResultFound:
        return False