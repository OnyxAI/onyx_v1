# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from onyx.api.assets import Json
from onyx.client.speech.assets import snowboydecoder
import onyx, importlib, wave, pyaudio, sys, os, pygame
from onyx.config import get_config
from onyxbabel import gettext
from onyx.util import play_wav
from onyx.skills.core import OnyxSkill
from onyx.client.stt import STTFactory

config = get_config('onyx')

skills = OnyxSkill(name="speech")

stt = STTFactory.create()

json = Json()
import speech_recognition as sr


class Detector:

	def __init__(self):
		self.lang = config.get('Base', 'lang')

	def detected_callback(self):
		play_wav(onyx.__path__[0] + "/client/speech/resources/ding.wav")
		while pygame.mixer.get_busy():
			pass

		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source)

		try:
			result = stt.execute(audio, language=str(self.lang))
			print("You said: " + result)
			skills.text = result
			skills.get_response()
		except sr.UnknownValueError:
			print("Speech Recognition could not understand audio")
		except sr.RequestError as e:
			print("Could not request results from Speech Recognition service; {0}".format(e))

	def start(self):
		detector = snowboydecoder.HotwordDetector(onyx.__path__[0] + "/client/speech/Onyx.pmdl", sensitivity=0.5, audio_gain=1)
		print('Starting...')
		detector.start(self.detected_callback)



if __name__ == "__main__":
	detector = Detector()
	detector.start()
