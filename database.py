# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

"""Application configuration."""
from onyx.app_config import Config

import sqlite3

from onyx import *

app = create_app()

connection = sqlite3.connect(Config.ONYX_PATH + '/db/data.db')
cursor = connection.cursor()
cursor.execute("""SELECT value FROM Config WHERE config='lang'""")
lang_raw = cursor.fetchone()

if lang_raw == None:
    data = {"config" : "lang", "value" : Config.LANG_FILE}
    cursor.execute("""INSERT INTO Config(config, value) VALUES(:config, :value)""", data)
    connection.commit()
    print('Database is now set.')
else:
    print('Database was already set up.')