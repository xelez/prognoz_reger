# -*- coding: utf-8 -*-
import config
import md5

# MySQL part
import sys

import MySQLdb
import MySQLdb.cursors

try:
    if config.use_mysql:
        conn = MySQLdb.connect (host = config.mysql_host,
                                port = config.mysql_port,
                                user = config.mysql_user,
                                passwd = config.mysql_passwd,
                                db = config.mysql_name,
                                cursorclass=MySQLdb.cursors.DictCursor,
                                use_unicode = True,
                                charset = 'utf8'
                               )
        sql_cursor = conn.cursor()
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)

def addslashes(s):
    d = {u'"':u'\\"', u"'":u"\\'", u"\0":u"\\\0", u"\\":u"\\\\"}
    return u''.join(d.get(c, c) for c in s)

def passwd_hash(user, passwd):
    return md5.new(addslashes(user.lower())+'#RANDOM_SEED#'+addslashes(passwd)).hexdigest();

def db_insert(table, data):
    query = u"""INSERT INTO `{table}` ({keys}) VALUES({values})""".format(
        table = table,
        keys = u','.join( ["`%s`" % key for key in data.keys()] ),
        values = u'%s,' * (len(data) -1) + u'%s',
    )
    if config.mysql_dry_run:
        return 0;
    sql_cursor.execute(query, data.values());
    return sql_cursor.lastrowid;


