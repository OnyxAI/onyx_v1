# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""


import time, sys, os, onyx, importlib
from flask import g, current_app as app, url_for

from onyx.api.assets import Json
from onyxbabel import gettext
from onyx.util.log import getLogger
from onyx.api.exceptions import *
from onyx.config import get_config

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

from onyx.api.parsers import Parser
from onyx.api.injector import Injector

from onyx.messagebus.client.ws import WebsocketClient
from onyx.messagebus.message import Message

from onyx import *

parser = Parser()
injector = Injector()

LOG = getLogger('Kernel')
config = get_config('onyx')
json = Json()

class Kernel:

    def __init__(self):
        self.kernel = self.set()
        self.app = app
        self.id = None
        self.text = None
        self.label = None
        self.kwargs = None
        self.url = None
        self.type_event = None

    def set(self):
        try:
            kernel = ChatBot("Onyx",
                storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
                logic_adapters=[
                    {
                        'import_path': 'onyx.api.kernel.adapters.best_adapter.BestMatchAdapter'
                    }
                ],
                input_adapter="chatterbot.input.VariableInputTypeAdapter",
                output_adapter="chatterbot.output.OutputAdapter",
                output_format="text",
                #database='database-bot-fr'
                database=onyx.__path__[0] + "/db/bot_data_" + config.get('Base', 'lang') + ".db"
            )

            return kernel
        except Exception as e:
            LOG.error('Error Set Kernel : ' + str(e))
            pass

    def train(self, kernel):
        try:
            kernel.set_trainer(ListTrainer)

            json.path = onyx.__path__[0] + "/data/sentences/" + config.get('Base', 'lang') + "/sentences.json"
            sentences = json.decode_path()
            for sentence in sentences:
                for query in sentence['sentences']:
                    kernel.train([
                        query['text'],
                        "%URL:" + sentence['url'] + "%"
                    ])

            json.path = onyx.__path__[0] + "/data/answers/" + config.get('Base', 'lang') + "/answers.json"
            answers = json.decode_path()
            for answer in answers:
                for query in answer['answers']:
                    kernel.train([
                        answer['label'],
                        query['text']

                    ])

            kernel.set_trainer(ChatterBotCorpusTrainer)
            try:
                kernel.train(
                    onyx.__path__[0] + "/data/sentences/" + config.get('Base', 'lang') + "/"
                )
            except:
                pass

            LOG.info('Kernel was train successfully')
        except Exception as e:
            LOG.error('Error Kernel Training : ' + str(e))
            pass


    def get(self):
        try:
            text = self.text

            parser.text = text
            json.json = parser.parse()

            parsed_request = json.decode()
            remplaced_str = parsed_request['remplaced_str']

            response = str(self.kernel.get_response(remplaced_str))

            if response.startswith("%URL:") and response.endswith("%"):
                self.url = response.replace("%URL:","").replace("%","")
                self.kwargs = parsed_request['kwargs']
                return self.get_event()
            else:
                return json.encode({"status":"success", "text":response})
        except Exception as e:
            LOG.error('Getting Sentence error : ' + str(e))
            text = str(self.kernel.get_response('error'))
            return json.encode({"status":"error", "text":text})

    def get_event(self):
        try:
            function = getattr(importlib.import_module(self.app.view_functions[self.url].__module__), self.app.view_functions[self.url].__name__)
            try:
                execute = function(self.kwargs)
            except:
                try:
                    execute = function()
                except:
                    execute = json.encode({"status":"error", "label":"error"})

            json.json = execute
            result = json.decode()

            text = str(self.kernel.get_response(result['label']))

            injector.text = text
            try:
                injector.scope = result['scope']
            except:
                pass

            json.json = injector.inject()
            final_result = json.decode()
            response = final_result['remplaced_str']

            return json.encode({"status":"success", "text":response})
        except Exception as e:
            LOG.error('Getting Response error : ' + str(e))
            text = str(self.kernel.get_response('error'))
            return json.encode({"status":"error", "text":text})
