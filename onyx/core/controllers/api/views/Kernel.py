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
from flask import request, Response
from onyx.decorators import api_required
#from onyx.api.kernel import Kernel
from onyx.api.assets import Json

json = Json()
#kernel_function = Kernel()

"""
@api.route('kernel', methods=['POST'])
@api_required
def kernel():
    if request.method == 'POST':
        try:
            kernel_function.text = request.form['text']
            result = kernel_function.get()
            json.json = result
            data = json.decode()
            return Response(json.encode({"text": data['text']}), mimetype='application/json')
        except Exception as e:
            return Response(json.encode({"status": "error"}), mimetype='application/json')

@api.route('train_kernel')
@api_required
def train_kernel():
    try:
        bot = kernel_function.set()
        kernel_function.train(bot)

        return Response(json.encode({"status": "success", "message": "Kernel was train successfully"}), mimetype='application/json')
    except Exception as e:
        return Response(json.encode({"status": "error"}), mimetype='application/json')
"""