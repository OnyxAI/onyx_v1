#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx import *
from werkzeug.contrib.fixers import ProxyFix

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)

blueprints_fabrics(app, get_blueprints(app))
error_pages(app)

if __name__ == "__main__":
    app.run()
