# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask_login import current_user
from onyx.core.models import *
from onyxbabel import gettext


def get_nav():
  try:
    navbar = []
    query = NavbarModel.Navbar.query.filter_by(idAccount=current_user.id).limit(11)
    for key in query:
      e = {}
      e['id'] = key.id
      e['fa'] = key.fa
      e['url'] = key.url
      e['pourcentage'] = key.pourcentage
      e['tooltip'] =  gettext(key.tooltip)
      navbar.append(e)
    return navbar
  except:
    return 0

def get_list():
  try:
    list = []
    query = NavbarModel.Navbar.query.filter(NavbarModel.Navbar.idAccount.endswith(str(current_user.id)))
    for fetch in query:
      e = {}
      e['id'] = fetch.id
      e['fa'] = fetch.fa
      e['url'] = fetch.url
      e['tooltip'] = fetch.tooltip
      list.append(e)
    return list
  except:
    return 0
