# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function


from doctor_service.core.tests import BaseTestCase

class UserApiTestCase(BaseTestCase):

    def setUp(self):
        super(UserApiTestCase, self).setUp()

    def test_book_appointment_no_conflict(self):
        self.client.post('/appointment/book', data=dict())
