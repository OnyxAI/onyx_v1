# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from .. import core
from flask import render_template, current_app as app, request, redirect, url_for, flash
from onyxbabel import gettext
from flask.ext.login import login_required
import importlib
from onyx.api.widgets import *

box = Widgets()

@core.route('widgets', methods=['GET','POST'])
@login_required
def widgets():
    if request.method == 'GET':
        json.json = box.get_list()
        list = json.decode()
        json.json = box.get()
        boxs = json.decode()
        return render_template('widgets/index.html', list=list, boxs=boxs)
    try:
        elements = request.form['box'].split('|')
        box.color = "blue-grey darken-1"
        box.url = elements[1]
        box.name = elements[0]
        box.see_more = elements[2]
        box.add()
        flash(gettext('Added Successfuly !'), 'success')
        return redirect(url_for('core.widgets'))
    except WidgetException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.widgets'))

@core.route('widgets/delete/<int:id>')
@login_required
def widget_delete(id):
    try:
        box.id = id
        box.delete()
        flash(gettext('Deleted with success !'), 'success')
        return redirect(url_for('core.widgets'))
    except WidgetException:
        flash(gettext('An error has occured !'), 'error')
        return redirect(url_for('core.widgets'))

@core.context_processor
def utility_processor():
    def get_widget(url):
        function = getattr(importlib.import_module(app.view_functions[url].__module__), app.view_functions[url].__name__)
        execute = function()
        return execute
    return dict(get_widget=get_widget)
