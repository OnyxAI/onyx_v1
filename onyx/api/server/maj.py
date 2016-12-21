"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import pip, imp
from flask import redirect, url_for, flash, request
from onyxbabel import gettext
from onyx.extensions import db

def maj_pip():
	try:
		pip.main(['install', '--upgrade' , "onyxproject"])
		migrateDB()
		flash(gettext("Onyx is now upgrade !"),'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext("An error has occured !"), 'error')
		return redirect(url_for('core.options'))

def migrateDB():
	try:
		from onyx.flask_config import SQLALCHEMY_DATABASE_URI
		from onyx.flask_config import SQLALCHEMY_MIGRATE_REPO
		from migrate.versioning import api
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO,tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(v))
		flash(gettext("Onyx is now upgrade !"),'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext("An error has occured !"), 'error')
		return redirect(url_for('core.options'))