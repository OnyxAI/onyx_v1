# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.machine import *
from onyx.core.models import *
import json
import pytest

machine = Machine()

@pytest.mark.usefixtures('db')
class Test_Machine:

    def test_get_machines(self):
        delete_machine = MachineModel.Machine(name='boo', house='foo', host='192.168.0.20', room='Bedroom')
        db.session.add(delete_machine)
        db.session.commit()

        result = json.loads(machine.get())

        assert result[0]['name'] == 'boo'

    def test_add_machines(self):
        machine.house = 'foo'
        machine.name = 'boo'
        machine.host = '192.128.0.20'
        machine.room = 'Bedroom'
        result = json.loads(machine.add())

        assert result['status'] == 'success'

    def test_delete_machines(self, db):
        delete_machine = MachineModel.Machine(name='boo', house='foo', host='192.168.0.20', room='Bedroom')
        db.session.add(delete_machine)
        db.session.commit()

        machine.id = delete_machine.id
        result = json.loads(machine.delete())
        assert result['status'] == 'success'
