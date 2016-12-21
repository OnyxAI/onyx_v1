"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France 
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from flask import render_template , request
import wikipedia

def getArticle():
	try:
		wikipedia.set_lang("fr")
		article = wikipedia.page(request.form['search'])
		return render_template('wiki/result.html', head=article.title, url=article.url, summary=wikipedia.summary(request.form['search']))
	except:
		return render_template('wiki/result.html', head="Erreur", summary="Ce que vous avez recherché n'existe pas sur wikipedia fr !")