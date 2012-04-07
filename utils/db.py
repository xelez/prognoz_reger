# -*- coding: utf-8 -*-

import config

from pymongo import Connection

connection = Connection(config.mongo_host, config.mongo_port)
db = connection[ config.mongo_name ]

def counter(name):
    '''Increment a counter stored in db and return its value.'''
    ret = db['counters'].find_and_modify(query = {'_id': name}, update = {'$inc': {'next': 1}}, new = True, upsert = True)
    return ret['next']


