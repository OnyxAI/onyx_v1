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
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from onyx.api.kernel import Kernel
from onyxbabel import gettext
from onyx.api.assets import Json

json = Json()
kernel_function = Kernel()

@api.route('kernel', methods=['GET','POST'])
def kernel():
    if request.method == 'POST':
        try:
            kernel_function.text = request.form['text']
            result = kernel_function.get()
            json.json = result
            data = json.decode()
            return data['text']
        except Exception as e:
            return gettext('An error has occured !')

@api.route('train_kernel')
def train_kernel():
    try:
        bot = kernel_function.set()
        kernel_function.train(bot)
        return gettext('Kernel was train successfully')
        return redirect(url_for('core.index'))
    except Exception as e:
        return gettext('An error has occured !')
