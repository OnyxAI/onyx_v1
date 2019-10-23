# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import api
from flask import  request
from onyx.decorators import api_required
from onyx.api.wiki import Wikipedia
from onyx.api.assets import Json
from onyx.api.exceptions import *

wikipedia = Wikipedia()
json = Json()

@api.route('wiki', methods=['POST'])
@api_required
def wiki():
    if request.method == 'POST':
        try:
            wikipedia.lang = "en-US" # CHANGE THIS
            wikipedia.search = request.form['search']
            article = wikipedia.get_article()
            summary = wikipedia.get_summary()

            return json.encode({"status": "success", "article": article, "summary": summary})
        except WikiException:
            return json.encode({"status": "error"})
