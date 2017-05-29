# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import json

class Message(object):
    def __init__(self, type, data={}, context=None):
        self.type = type
        self.data = data
        self.context = context

    def serialize(self):
        return json.dumps({
            'type': self.type,
            'data': self.data,
            'context': self.context
        })

    @staticmethod
    def deserialize(value):
        obj = json.loads(value)
        return Message(obj.get('type'), obj.get('data'), obj.get('context'))

    def reply(self, type, data, context={}):
        new_context = self.context if self.context else {}
        for key in context:
            new_context[key] = context[key]
        if 'target' in data:
            new_context['target'] = data['target']
        elif 'client_name' in context:
            context['target'] = context['client_name']
        return Message(type, data, context=new_context)

    def publish(self, type, data, context={}):
        new_context = self.context.copy() if self.context else {}
        for key in context:
            new_context[key] = context[key]

        if 'target' in new_context:
            del new_context['target']

        return Message(type, data, context=new_context)
