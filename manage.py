# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from flask.ext.script import Manager, Server

import doctor_service.settings as settings
from doctor_service.app import create_app

app = create_app(config=settings.Development)
manager = Manager(app)
manager.add_command('runserver', Server(threaded=True))


@manager.command
def test():
    import subprocess
    command = 'nosetests --with-xunit --with-coverage --cover-package=doctor_service --cover-erase'.split(' ')
    subprocess.call(command)

if __name__ == "__main__":
    manager.run()
