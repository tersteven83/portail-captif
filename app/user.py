from flask import (Blueprint, render_template, request, flash, redirect,
                   url_for)
from sqlalchemy import and_
from .models import Radacct, Radcheck, Userinfo
from . import db, generate_passcode, hash_password, verify_password, sendSMS, format_tel_number
from .auth import is_valid_phone_number
import re
from . import config


bp = Blueprint("user", __name__, url_prefix='/user')
@bp.route('/add_wk/<ID>/<int:is_session>', methods=["POST", "GET"])
def add_work_phone(ID, is_session):
    """
    ajouter un numéro de téléphone
    :param ID: id de l'utilisateur ou id de la session
    :param is_session: 0|1 1 si c'est lors d'une session active que l'utilisateur veut ajouter son tel
    """
    if is_session == 1:
        session_is_active, sessionInfo = session_state(ID)
        if session_is_active:
            username = sessionInfo.username
            
            if request.method == "POST":
                tel = request.form.get("tel")
                if is_valid_phone_number(tel):
                    tel = format_tel_number(tel)
                    user_info = Userinfo.query.filter(Userinfo.username == username).one_or_none()
                    user_info.workphone = tel
                    db.session.commit()
                    flash("Votre numéro a été bien enregistré", category='message')
                    return redirect(url_for('user.valide_modification', acctsessionId=ID))
                else:
                    flash("Veuillez vérifier votre saisi", category='error')
            
            return render_template('user/add_work_phone.html')
    
    else:
        user_info = Userinfo.query.filter_by(id=ID).one_or_none()
        if user_info and user_info.can_be_edited:
            if request.method == "POST":
                tel = request.form.get("tel")
                if is_valid_phone_number(tel):
                    tel = format_tel_number(tel)
                    user_info.workphone = tel
                    flash("Votre numéro a été bien enregistré", category='message')
                    
                    # generé un passcode au nouveau numéro téléphone
                    tmp_passcode = str(generate_passcode())
                    user_info.tmp_passcode = tmp_passcode

                    # Envoyer le passcode à l'utilisateur
                    msg = f"Votre pass code de réinitialisation de mot de passe : {tmp_passcode}"
                    if sendSMS(msg, tel):
                    # if 1:
                        print(msg)
                        # user_info.can_be_edited = False
                        db.session.commit()
                        return redirect(url_for('user.forgot_pwd', user_id=ID))
                    else:
                        print("le code n'est pas envoyé")
                else:
                    flash("Veuillez vérifier votre saisi", category='error')
            
            return render_template('user/add_work_phone.html', user_info=user_info)
        else:
            return  '404 error not found', 404
    

@bp.route('/edit_pwd/<acctsessionId>', methods=['GET', 'POST'])
def edit_pwd(acctsessionId):
    # on vérifie si la session existe dans la base de donnée
    session_is_active, sessionInfo = session_state(acctsessionId)
    if session_is_active:
        # la session existe
        username = sessionInfo.username
        if request.method == 'POST': 
            old_passd = request.form.get('oldPassd')
            new_passd = request.form.get('newPassd')
            cnf_passd = request.form.get('cnfPassd')
            
            # vérifier si le password utilisé par l'utilisateur est le même que celle dans le BD
            # connaitre l'attribut *-Password dans la BD, quelle methode est utilisé pour le crypté
            user_check_passd = Radcheck.query.filter(
                and_(
                    Radcheck.username == username,
                    Radcheck.attribute.like("%-Password")
                )
            ).one()
            password_attr = user_check_passd.attribute[:-9].lower()
            password_value = user_check_passd.value
            if password_is_correct(old_passd, password_value, password_attr) and new_passd == cnf_passd:
                # bool(re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", new_passd)):
                # hasher le nouveau password
                hash_pwd = hash_password(new_passd)
                user_check_passd.value = hash_pwd
                user_check_passd.attribute = "SHA-Password"
                db.session.commit()
                # flash("Votre nouveau mot de passe a bien été enregistré", category='message')
                return redirect(f"http://{config.ip_pfsense}:8002/index.php?zone={config.zone}")
                
                
            else:
                # print(old_passd + " " + new_passd + " " + cnf_passd)
                flash("Les mots de passes que vous avez saisi ne sont pas correctes.")
        return render_template('user/edit_pwd.html', username=username)
        

@bp.route('/fg_pwd/<int:user_id>', methods=['GET', 'POST'])
def forgot_pwd(user_id):
    """
        Mot de passe oublié
    """
    user_info = Userinfo.query.filter_by(id=user_id).one_or_none()
    
    # vérifier si l'utilisateur est modifiable
    if user_info and user_info.can_be_edited:
        if request.method == "POST":
            pass_code = request.form.get("passCode")
            new_passd = request.form.get("newPassd")
            cnf_passd = request.form.get("cnfPassd")
            
            # vérifier si le passcode entré par l'utilisateur est le même que celle dans la BD,
            # les deux passwords sont égaux,
            # les password sont conformes aux normes
            if user_info.tmp_passcode == pass_code and new_passd == cnf_passd:
                # bool(re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", new_passd)):
                
                # hasher le nouveau password
                hash_pwd = hash_password(new_passd)
                Radcheck.query.filter(
                    and_(
                        Radcheck.username == user_info.username,
                        Radcheck.attribute.like("%-Password")
                    )
                ).update({
                    Radcheck.attribute: "SHA-Password",
                    Radcheck.value: hash_pwd
                })
                
                # make all userinfos that have the same work phone uneditable
                Userinfo.query.filter(Userinfo.workphone == user_info.workphone).update({
                    Userinfo.can_be_edited: False
                })
                db.session.commit()
                return redirect(f"http://{config.ip_pfsense}:8002/index.php?zone={config.zone}")
            else:
                flash("Le code que vous avez entré est invalide. Veuillez vérifier votre saisi et/ou consulter votre telephone", category='error')
            
        return render_template('user/fg_pwd.html', username=user_info.username)       
    else:
        return "You can not edit this user"
        
def session_state(acctsessionId):
    # on vérifie si la session existe dans la base de donnée
    sessionInfo = Radacct.query.\
        filter(
            Radacct.acctsessionid == acctsessionId,
            Radacct.acctstoptime == None
        ).one_or_none()
    if sessionInfo:
        return True, sessionInfo
    return False, None

def password_is_correct(verify, target, method="cleartext") -> bool:
    """
        This method is used to verify if the verifying password matched to target pasword
        @params target: the target password
        @params verify: the password to verify
        @method method: this method accepts one of "cleartext, sha", default is "cleartext"
    """
    if method == "cleartext":
        return target == verify
    elif method == "sha":
        return verify_password(verify, target)