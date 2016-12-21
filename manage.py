"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import json
from flask_script import Manager , Server
from flask_migrate import MigrateCommand
from onyx import create_app
from onyx.extensions import db


manager = Manager(create_app)


if __name__ == "__main__":
    manager.run()