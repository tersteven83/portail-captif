from flask import (Blueprint, render_template, request, flash, redirect,
                   url_for, g)
from sqlalchemy import and_
from .models import Radacct, Radcheck, Userinfo
from . import db, generate_passcode, hash_password
from .auth import is_valid_phone_number
import re


bp = Blueprint("user", __name__, url_prefix='/user')

@bp.route('/edit/<acctsessionId>', methods=['POST', 'GET'])
def edit(acctsessionId):
        # on vérifie si la session existe dans la base de donnée
    session_is_active, sessionInfo = session_state(acctsessionId)
    if session_is_active:
        # la session existe
        username = sessionInfo.username
        if request.method == 'POST':
            error = None
            success = None
            # Vérifier si l'username n'est pas vide
            newUsername = request.form.get('newUsername')
            # si le nouveau username n'est pas vide et n'existe pas dans la base de donnée
            # on modifie l'ancien username par ce dernier
            if newUsername and not Radcheck.query.filter(Radcheck.username == newUsername).all():
                # vérifier si le nouveau nom est alpha-numérique
                if bool(re.match("^(?=.*[a-zA-Z])[a-zA-Z0-9_]+$", newUsername)) == True:
                    userCheckInfos = Radcheck.query.filter(Radcheck.username == username)
                    
                    # récuperer tous les ID portant l'username à modifier
                    ids = []
                    for userCheckInfo in userCheckInfos:
                        ids.append(userCheckInfo.id)
                        
                    # Modifier l'username de ces IDs au nouveau username
                    while (len(ids) > 0):
                        Radcheck.query.filter(Radcheck.id == ids.pop()).\
                            update({Radcheck.username:newUsername})
                        
                    userAccts = Radacct.query.filter(Radacct.username == username)
                    
                    for userAcct in userAccts:
                        ids.append(userAcct.radacctid)
                        
                    while (len(ids) > 0):
                        Radacct.query.filter(Radacct.radacctid == ids.pop()).\
                            update({Radacct.username:newUsername})   
                        
                    Radacct.query.filter(Radacct.acctsessionid == acctsessionId).\
                        update({Radacct.username: newUsername})
                    
                    # mettre à jour l'username 
                    username = newUsername
                else:
                    error = "match username misy diso"
            else:
                error = "Utilisateur déjà existant."
                
            if error is not None:
                flash(error)
            else:
                new_passd = request.form.get('newPassd')
                cnf_passd = request.form.get('cnfPassd')
                print("new mdp: " + new_passd + " cnf pwd: " + cnf_passd)
                # vérifier si les deux password sont les mêmes
                if new_passd and bool(re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", new_passd)):
                    if new_passd == cnf_passd:
                        hash_pwd = hash_password(new_passd)
                        Radcheck.query.filter(
                            and_(
                                Radcheck.username == username,
                                Radcheck.attribute.like("%-Password")
                            )
                        ).update({
                            Radcheck.attribute: "SHA-Password",
                            Radcheck.value: hash_pwd
                        })
                    else:
                        error = "Les deux mots de passes doivent être les mêmes"
                else:
                    error = "Tsy mitovy le mot de passe"
                
                if error is not None:
                    flash(error)
                else:
                    flash("Votre modification est bien enregistrée.", category='message')
                    # db.session.commit()
                
        return render_template('user/edit.html')     
    else:
        return "null"

@bp.route("/valid/<acctsessionId>", methods=["GET", "POST"])
def valide_modification(acctsessionId):
    session_is_active, sessionInfo = session_state(acctsessionId)
    if session_is_active:
        # la session existe
        username = sessionInfo.username
        
        # récupérer son work phone
        user_info = Userinfo.query.filter(Userinfo.username == username).one_or_none()
        if request.method == "POST":
            pass_code = request.form.get("passCode")
            # vérifier si le passcode entré par l'utilisateur est le même que celle dans la BD
            if user_info.tmp_passcode == pass_code:
                flash("Code vérifiée avec succés.", category='message')
                return redirect(url_for('user.edit', acctsessionId=acctsessionId))
            else:
                flash("Le code que vous avez entré est invalide. Veuillez vérifier votre saisi et/ou consulter votre \
                    telephone", category='error')
            
                
        
        # request.method == "GET"
        else:
            wk_phone = user_info.workphone
            # envoyer le passcode aux work phone de l'utilisateur
            if wk_phone:
                # générer un passcode et enregistrer dans la table userinfo
                # et puis c'est de là que l'on va vérifier la crédibilité de l'utilisateur
                tmp_passcode = str(generate_passcode())
                user_info.tmp_passcode = tmp_passcode
                
                # Envoyer le passcode à l'utilisateur
                msg = f"Veuillez confirmez votre identification via ce code : {tmp_passcode}"
                # if sendSMS(msg, wk_phone):
                if 1:
                    print('ok')
                    flash("Veuillez entrer le passcode envoyé au numéro +**********{}".format(wk_phone[-2:]))
                    db.session.commit()
                else:
                    print("le code n'est pas envoyé")
                
            else:
                return redirect(url_for('user.add_work_phone', acctsessionId=acctsessionId))
            
        return render_template('user/valid.html')
      

@bp.route('/add_wk/<ID>/<int:is_session>', methods=["POST", "GET"])
def add_work_phone(ID, is_session):
    if is_session == 1:
        session_is_active, sessionInfo = session_state(ID)
        if session_is_active:
            username = sessionInfo.username
            
            if request.method == "POST":
                tel = request.form.get("tel")
                if is_valid_phone_number(tel):
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
                    user_info.workphone = tel
                    flash("Votre numéro a été bien enregistré", category='message')
                    
                    # generé un passcode au nouveau numéro téléphone
                    tmp_passcode = str(generate_passcode())
                    user_info.tmp_passcode = tmp_passcode

                    # Envoyer le passcode à l'utilisateur
                    msg = f"Votre pass code de réinitialisation de mot de passe : {tmp_passcode}"
                    # if sendSMS(msg, wk_phone):
                    if 1:
                        print(msg)
                        # user_info.can_be_edited = False
                        db.session.commit()
                        return redirect(url_for('user.edit_pwd', user_id=ID))
                    else:
                        print("le code n'est pas envoyé")
                else:
                    flash("Veuillez vérifier votre saisi", category='error')
            
            return render_template('user/add_work_phone.html', user_info=user_info)
        else:
            return  user_info.__str__()
    

@bp.route('/edit_pwd/<int:user_id>', methods=['GET', 'POST'])
def edit_pwd(user_id):
    """
        Modifier le mot de passe de l'utilisateur
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
            if user_info.tmp_passcode == pass_code and new_passd == cnf_passd and \
                bool(re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", new_passd)):
                
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
                
                # make the userinfo ineditable
                user_info.can_be_edited = False
                db.session.commit()
                return redirect("192.168.110.0:8002/index.php?zone=ambohijatovo")
            else:
                flash("Le code que vous avez entré est invalide. Veuillez vérifier votre saisi et/ou consulter votre \
                    telephone", category='error')
            
        return render_template('user/edit_pwd.html', username=user_info.username)       
    else:
        return "request.headers('404')"
        
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