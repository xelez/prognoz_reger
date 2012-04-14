# -*- coding: utf-8 -*-

from utils.mysql import sql_cursor, db_insert, passwd_hash
import time

def delete_user(uid):
    sql_cursor.execute('DELETE FROM `user` WHERE id=%s', uid)
    sql_cursor.execute('DELETE FROM `usergroup` WHERE user_id=%s', uid)
    sql_cursor.execute('DELETE FROM `tester_solutions` WHERE user_id=%s', uid)

def add_user(name, login, passwd=u'123456', access=1, email=u'noreply@localhost', authorized=1):
    return db_insert(u'user', {
        u'name'       : name,
        u'login'      : login,
        u'password'   : passwd_hash(login, passwd),
        u'access'     : access,
        u'email'      : email,
        u'authorized' : authorized,
        u'settings'   : '',
        u'timestamp'  : int(time.time()),
        })

def user_addgroup(uid, gid):
    return db_insert(u'usergroup', {
        u'user_id'  : uid,
        u'group_id' : gid,
        })

