# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import api
from flask import render_template, request, g
from flask.ext.login import login_required
from onyx.api.wiki import Wikipedia
from onyxbabel import gettext
from onyx.api.exceptions import *

wikipedia = Wikipedia()

@api.route('wiki', methods=['GET', 'POST'])
@login_required
def wiki():
    if request.method == 'POST':
    	"""
		@api {post} /wiki Request Wiki Article
		@apiName getArticle
		@apiGroup Wiki
		@apiPermission authenticated

		@apiParam {String} search Search Input

		@apiSuccess (200) {Object[]} article List
		@apiSuccess (200) {String} article.head Header of Article
		@apiSuccess (200) {String} article.url Url of Article
		@apiSuccess (200) {String} article.summary Article Content

		@apiError NoExist No Article Exist

		"""
        try:
            wikipedia.lang = g.lang
            wikipedia.search = request.form['search']
            article = wikipedia.get_article()
            summary = wikipedia.get_summary()
            return article
        except WikiException:
            return gettext("An error has occured !")
