# -*- coding: utf-8 -*-

from utils.templates import render
from utils.misc import webob_wrap, validate_user, gen_pwd
from utils.db import db, counter
from utils import gate

from webob import Response

from paste.urlmap import URLMap
from paste.fileapp import DirectoryApp

import config

@webob_wrap
def users_app(req):
    res = Response()
    users = db["teams"]
    
    u = users.find_one({'secret' : req.params.get('s', '')})

    res.unicode_body = render('users.html',
        newuser = u,
        users = users.find().sort('num'),
    )

    if u is not None:
        del u['secret']
        users.save(u)

    return res

@webob_wrap
def reg_app(req):
    res = Response()
    users = db["teams"]

    if req.method != 'POST':
        res.unicode_body = render('reg.html', user={})
        return res;

    #here method == 'POST'
    user = {
            'surname' : req.params.get('surname', ''),
            'name'    : req.params.get('name', ''),
            'school'  : req.params.get('school', ''),
            'year'    : req.params.get('year', ''),
        }

    if not validate_user(user):
        res.unicode_body = render('reg.html', user=user, error=u'Неверный формат введённых данных')
        return res;

    #user is valid, lets add him
    num = counter('users')
    login = config.login_fmt % num
    nickname = u"(%02d) %s %s" % (int(user['year']), user['surname'], user['name'])
    passwd = gen_pwd(config.passwd_len)

    uid = gate.add_user(nickname, login, passwd)
    gate.user_addgroup(uid, config.group_id)
    
    user['login'] = login
    user['passwd'] = passwd
    user['uid'] = uid
    user['secret'] = gen_pwd(13)
    users.insert(user);

    res.unicode_body = render('redirect.html', address='users?s=%s' % user['secret'])
    return res

root_map = URLMap()
root_map['/css/'] = DirectoryApp('./static/css/')
root_map['/img/'] = DirectoryApp('./static/img/')
root_map['/users'] = users_app
root_map['/reg']  = reg_app

root_app = root_map
