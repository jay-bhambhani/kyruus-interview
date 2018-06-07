# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function


def safe_get(cursor, sql, exception_message, **replacements):
    cursor.execute(sql, replacements)
    result = cursor.fetchone()
    if not result:
        raise Exception(exception_message.format(**replacements))
    else:
        return result
