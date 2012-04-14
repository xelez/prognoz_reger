# -*- coding: utf-8 -*-

from utils.templates import render
from utils.misc import webob_wrap, validate_user, gen_pwd
from utils.db import db, counter
from utils import gate

from webob import Response

from paste.auth.digest import digest_password, AuthDigestHandler
from paste.urlmap import URLMap
from paste.fileapp import DirectoryApp

import config

def authfunc(environ, realm, username):
        return digest_password(realm, config.admin_login, config.admin_passwd)

@webob_wrap
def users_app(req):
    res = Response()
    admin_mode = (req.environ.get('REMOTE_USER') == config.admin_login)
    users = db["teams"]

    del_login = req.params.get('del', '')
    if admin_mode and del_login!='':
        u = users.find_one({'login': del_login})
        if u is not None:
            gate.delete_user(u['uid'])
            users.remove({'_id': u['_id']})
            res.unicode_body = render('redirect.html', address='?')
            return res
            
    
    res.unicode_body = render('users.html',
        users = users.find().sort('num'),
        admin = admin_mode
    )

    return res

if config.admin_auth:
    usersadmin_app = AuthDigestHandler(users_app, 'Users Manage', authfunc)
else:
    usersadmin_app = users_app

@webob_wrap
def reg_app(req):
    res = Response()
    users = db["teams"]

    if req.method != 'POST':
        res.unicode_body = render('reg.html', user={}, newlogin = req.params.get('new'))
        return res;

    #here method == 'POST'
    user = {
            'surname' : req.params.get('surname', ''),
            'name'    : req.params.get('name', ''),
            'school'  : req.params.get('school', ''),
            'year'    : req.params.get('year', ''),
            'email'   : req.params.get('email', ''),
            'pass1'   : req.params.get('pass1', ''),
            'pass2'   : req.params.get('pass2', ''),
        }

    if not validate_user(user):
        res.unicode_body = render('reg.html', user=user, error=u'Неверный формат введённых данных')
        return res;

    #user is valid, lets add him
    num = counter('users')
    login = config.login_fmt % num
    nickname = u"(%02d) %s %s" % (int(user['year']), user['surname'], user['name'])
    
    uid = gate.add_user(nickname, login, user['pass1'], email = user['email'])
    gate.user_addgroup(uid, config.group_id)
    
    user['num'] = num
    user['login'] = login
    user['uid'] = uid
    users.insert(user);

    res.unicode_body = render('redirect.html', address='reg?new=%s' % login)
    return res

root_map = URLMap()
root_map['/users'] = users_app
root_map['/admin'] = usersadmin_app
root_map['/reg']  = reg_app

if config.serve_static:
    root_map['/css/'] = DirectoryApp('./static/css/')
    root_map['/img/'] = DirectoryApp('./static/img/')
    root_map['/js/']  = DirectoryApp('./static/js/')

root_app = root_map
