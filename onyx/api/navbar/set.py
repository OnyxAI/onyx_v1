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


def set_navbar(last,new):
  last_nav = NavbarModel.Navbar.query.filter_by(id=last).first()
  new_nav = NavbarModel.Navbar.query.filter_by(id=new).first()

  new_url = new_nav.url
  new_tooltip = new_nav.tooltip
  new_fa = new_nav.fa

  last_url = last_nav.url
  last_tooltip = last_nav.tooltip
  last_fa = last_nav.fa

  #Update New
  last_nav.url = new_url
  last_nav.tooltip = new_tooltip
  last_nav.fa = new_fa

  #Update Last
  new_nav.url = last_url
  new_nav.tooltip = last_tooltip
  new_nav.fa = last_fa

  #Update
  db.session.add(last_nav)
  db.session.commit()
  db.session.add(new_nav)
  db.session.commit()

  print('Done')
  return True

def set_plugin_navbar(folder):
  data = decodeJSON.decode_navbar_plugin(folder)
  user = UsersModel.User.query.all()
  for key in user:
    for nav in data:
      query = NavbarModel.Navbar(idAccount=key.id,fa=nav['fa'],url=nav['url'],tooltip=nav['tooltip'])
      db.session.add(query)
      db.session.commit()
  print('Set Done')

def set_plugin_navbar_user(folder,username):
  data = decodeJSON.decode_navbar_plugin(folder)
  user = UsersModel.User.query.filter_by(username=username).first()
  for nav in data:
    query = NavbarModel.Navbar(idAccount=user.id,fa=nav['fa'],url=nav['url'],tooltip=nav['tooltip'])
    db.session.add(query)
    db.session.commit()
  print('Set Done')
