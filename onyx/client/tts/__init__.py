# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from abc import abstractmethod

import onyx, importlib
from onyx.config import get_config

config = get_config('onyx')

class TTS(object):

	def __init__(self, lang):
		self.lang = config.get('Base', 'lang')
		self.voice = None
		self.filename = '/tmp/tts.wav'

	def init(self, ws):
		self.ws = ws

	@abstractmethod
	def execute(self, sentence):
		pass

class TTSFactory(object):
    from onyx.client.tts.google_tts import GoogleTTS

    CLASSES = {
        "google": GoogleTTS
    }

    @staticmethod
    def create():

        module = config.get('TTS', 'default')
        lang = config.get('Base', 'lang')
        classe = TTSFactory.CLASSES.get(module)


        tts = classe(lang)

        return tts
