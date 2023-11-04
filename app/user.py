from flask import Blueprint, render_template
from . import db
from .models import Radacct, Userinfo

bp = Blueprint("user", __name__)

@bp.route('/dashboard/<acctuniqueId>')
def dashboard(acctuniqueId=None):
    if acctuniqueId is not None:
        # on vérifie si la session existe dans la base de donnée
        sessionInfo = Radacct.query.\
            filter(
                Radacct.acctuniqueid == acctuniqueId,
                Radacct.acctstoptime == None
            )
        
        if sessionInfo.count() == 1:
            # la session existe
            username = sessionInfo.one().username
            # checker si l'username contient le mot 'omnis_'
            if 'omnis_' in username:
                return render_template('user/guest.html')
            else:
                userinfo = Userinfo.query.filter(Userinfo.username == username).one()
                return render_template('user/dashboard.html', userinfo=userinfo)      
        else:
            return "null"
        
@bp.route('/dashboard/<acctuniqueId>/<username>')
def profile(acctuniqueId, username):
    return render_template('user/profile.html')

@bp.route("/disconnect", methods=['POST'])
def disconnect():
    print ("coucou")
    return "hello"