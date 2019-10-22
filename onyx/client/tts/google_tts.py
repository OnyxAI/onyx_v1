# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
#from gtts import gTTS
from onyx.client.tts import TTS
from onyx.util import play_mp3


class GoogleTTS(TTS):
    def __init__(self, lang):
        super(GoogleTTS, self).__init__(lang)

    def execute(self, sentence):
        try:
            tts = gTTS(sentence, self.lang)
            tts.save(self.filename)
            p = play_mp3(self.filename)
            p.communicate()
        except:
            p = play_mp3("http://translate.google.com/translate_tts?ie=utf8&tl=" + self.lang + "&client=tw-ob&q=" + sentence)
            p.communicate()
