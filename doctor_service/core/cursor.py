# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import os
from contextlib import contextmanager
import psycopg2
import psycopg2.extras

from config import config


@contextmanager
def get_kyruus_db_cursor():
    env = os.environ.get('env') # current
    conf = config.get(env)
    postgres_conf = conf['postgres']
    database = postgres_conf.get('db')
    username = postgres_conf.get('user')
    pw = postgres_conf.get('pw')
    conn = psycopg2.connect('dbname={db} user={u} password={w}'.format(db=database, u=username, w=pw))
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cursor
