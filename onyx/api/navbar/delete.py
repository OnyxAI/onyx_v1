# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.core.models import *
from onyx.extensions import db
from onyx.api.assets import decodeJSON


def delete_plugin_navbar(folder):
  data = decodeJSON.decode_navbar_plugin(folder)
  user = UsersModel.User.query.all()
  for key in user:
    for nav in data:
      query = NavbarModel.Navbar.query.filter_by(idAccount=key.id,tooltip=nav['tooltip']).first()
      query.url = None
      query.tooltip = "Undefined"
      query.fa = None
      db.session.add(query)
      db.session.commit()
  print('Set Done')
