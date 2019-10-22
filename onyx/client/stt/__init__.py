# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from abc import abstractmethod

from speech_recognition import Recognizer
from onyx.config import get_config

config = get_config('onyx')

class STT(object):

    def __init__(self):
        self.lang = config.get("Base", "lang")
        self.recognizer = Recognizer()

    @abstractmethod
    def execute(self, audio, language=None):
        pass


class TokenSTT(STT):

    def __init__(self):
        super(TokenSTT, self).__init__()
        self.token = None


class GoogleSTT(TokenSTT):
    def __init__(self):
        super(GoogleSTT, self).__init__()


    def execute(self, audio, language=None):
        language = language or self.lang
        return self.recognizer.recognize_google(audio, self.token, str(language))


class STTFactory(object):
    CLASSES = {
        "google": GoogleSTT
    }

    @staticmethod
    def create():
        module = config.get("STT", "default")
        classe = STTFactory.CLASSES.get(module)
        return classe()
