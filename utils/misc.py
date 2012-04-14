# -*- coding: utf-8 -*-

from webob import Request
from webob.exc import HTTPNotFound

from exceptions import ValueError
import re

import string
import random

name_re = re.compile(u'''^[-а-яА-ЯёЁ]+$''')
school_re = re.compile(u'''^[\\Q-_№., "'\\Eа-яА-ЯёЁa-zA-Z0-9]+$''')

#Regex for checking email from Django.. This is just magic.. with smiles in second string ^_`
email_re = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
            r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

email_maxlen = 40
name_maxlen = 40
school_maxlen = 40
pwd_minlen = 5

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

def check_field(field, match_re, maxlen):
    return (len(field) <= maxlen) and (match_re.match(field) is not None)

def validate_user(user):
    if not check_field(user['name'], name_re, name_maxlen):
        return False;
    
    if not check_field(user['surname'], name_re, name_maxlen):
        return False;

    if not check_field(user['school'], school_re, school_maxlen):
        return False;
    
    if not check_field(user['email'], email_re, email_maxlen):
        return False;

    if (user['pass1'] != user['pass2']) or (len(user['pass1']) < pwd_minlen):
        return False;

    try:
        if not ( 0 < int(user['year']) < 12):
            return False;
    except ValueError:
        return False;
    
    return True;


