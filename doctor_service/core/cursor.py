# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import os
from contextlib import contextmanager
import psycopg2
import psycopg2.extras


@contextmanager
def get_kyruus_db_cursor():
    database = os.environ.get('KYRUUS_DB_NAME')
    username = os.environ.get('KYRUUS_USER_NAME')
    pw = os.environ.get('KYRUUS_DB_PASSWORD')
    conn = psycopg2.connect('dbname={db} user={u} password={w}'.format(db=database, u=username, w=pw))
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cursor
