# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.api.options import Options
from onyx.core.models import *
import json
import pytest

option = Options()

@pytest.mark.usefixtures('db', 'user_test_a')
class Test_Options:

    def test_set_account(self, user_test_a):

        option.user = user_test_a.id
        option.color = 'dark-blue'
        result = json.loads(option.set_account())

        assert result['status'] == 'success'
        assert user_test_a.buttonColor == 'dark-blue'
