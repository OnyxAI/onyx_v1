# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import onyx
from flask import current_app as app

from onyx.api.assets import Json
from onyx.util.log import getLogger
from onyx.api.exceptions import *
from onyx.config import get_config

from onyx.skills.core import *

#from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

LOG = getLogger('Kernel')
config = get_config('onyx')
json = Json()

"""
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
                storage_adapter="chatterbot.storage.SQLStorageAdapter",
                input_adapter="chatterbot.input.VariableInputTypeAdapter",
                output_adapter="chatterbot.output.OutputAdapter",
                output_format="text",
                database_uri="sqlite:///" + onyx.__path__[0] + "/db/bot_data_" + config.get('Base', 'lang') + ".db"
            )

            return kernel
        except Exception as e:
            LOG.error('Error Set Kernel : ' + str(e))
            raise KernelException(str(e))

    def train(self, kernel):
        try:
            trainer = ChatterBotCorpusTrainer(kernel)

            if config.get('Base', 'lang') == "fr_FR":
                trainer.train('chatterbot.corpus.french')
            else:
                trainer.train('chatterbot.corpus.english')

            
            trainer = ChatterBotCorpusTrainer(kernel)
            trainer.train(
                self.app.config['ONYX_PATH'] + "/data/sentences/" + config.get('Base', 'lang') + "/"
            )


            trainer = ListTrainer(kernel)
            json.path = self.app.config['ONYX_PATH'] + "/data/answers/" + config.get('Base', 'lang') + "/answers.json"
            answers = json.decode_path()
            for answer in answers:
                for query in answer['answers']:
                    trainer.train([
                        answer['label'],
                        query['text']
                    ])

            LOG.info('Skill Training')

            all_skill = get_raw_name(self.app.config['SKILL_FOLDER'])
            for skill in all_skill:
                try:
                    trainer = ListTrainer(kernel)

                    json.path = self.app.config['SKILL_FOLDER'] + skill + "/data/answers/" + config.get('Base', 'lang') + "/answers.json"
                    answers = json.decode_path()
                    for answer in answers:
                        for query in answer['answers']:
                            trainer.train([
                                answer['label'],
                                query['text']

                            ])

                    trainer = ChatterBotCorpusTrainer(kernel)
                    try:
                        trainer.train(
                            self.app.config['SKILL_FOLDER'] + skill + "/data/sentences/" + config.get('Base', 'lang') + "/"
                        )
                    except Exception as e:
                        LOG.error('Error Kernel Skill Training : ' + str(e))
                        pass
                except Exception as e:
                    LOG.error('Error Kernel Skill Training : ' + str(e))
                    pass

            LOG.info('Kernel was train successfully')
        except Exception as e:
            LOG.error('Error Kernel Training : ' + str(e))
            raise KernelException(str(e))


    def get(self):
        try:
            text = self.text

            response = self.kernel.get_response(text).text

            return json.encode({"status":"success", "text": response})
        except Exception as e:
            LOG.error('Getting Sentence error : ' + str(e))
            raise KernelException(str(e))
"""