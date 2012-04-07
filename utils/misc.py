# -*- coding: utf-8 -*-

from webob import Request
from webob.exc import HTTPNotFound

from exceptions import ValueError
import re

import string
import random

name_re = re.compile(u'^[а-яА-ЯёЁ]+$')
school_re = re.compile(u'^[ .,а-яА-ЯёЁ0-9]+$')

pwd_chars = string.letters + string.digits
pwd_len = 6

def webob_wrap(func):
    def wrapped(environ, start_response):
        req = Request(environ)
	req.charset = 'utf8'
        app = func(req)
        if app is None:
		app = HTTPNotFound(u'Нет такой страницы')
        return app(environ, start_response)
    return wrapped

def gen_pwd(pwdlen = 6):
    return ''.join(random.choice(pwd_chars) for _ in range(pwdlen))

def validate_user(user):
    if name_re.match(user['name']) is None:
        return False;
    
    if name_re.match(user['surname']) is None:
        return False;

    if school_re.match(user['school']) is None:
        return False;

    try:
        if not ( 0 < int(user['year']) < 12):
            return False;
    except ValueError:
        return False;
    
    return True;


