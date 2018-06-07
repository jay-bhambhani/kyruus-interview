# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from datetime import datetime
from datetime import timedelta
from doctor_service.core.tests import BaseTestCase

class UserApiTestCase(BaseTestCase):

    def setUp(self):
        super(UserApiTestCase, self).setUp()

    def test_book_appointment_no_conflict(self):
        now_time = datetime.now()
        self.client.post('/appointment/book', data=dict(doctor='test_doc',
                                                        location='test_loc',
                                                        day='M',
                                                        start_time=now_time.time(),
                                                        end_time=(now_time + timedelta(hours=1)).time()))
        assert c
