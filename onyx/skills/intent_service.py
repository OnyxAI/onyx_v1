# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani   
"""
from adapt.engine import IntentDeterminationEngine

from onyx.sockyx.message import Message
from onyx.skills.core import open_intent_envelope
from onyx.util.log import getLogger
from onyx.util.parse import normalize

logger = getLogger(__name__)


class IntentService(object):
    def __init__(self, emitter):
        self.engine = IntentDeterminationEngine()
        self.emitter = emitter
        self.emitter.on('register_vocab', self.handle_register_vocab)
        self.emitter.on('register_intent', self.handle_register_intent)

        self.emitter.on('onyx_recognizer:utterance', self.handle_utterance)

        self.emitter.on('detach_intent', self.handle_detach_intent)
        self.emitter.on('detach_skill', self.handle_detach_skill)

    def handle_utterance(self, message):

        lang = message.data.get('lang', None)
        if not lang:
            lang = "en-US"

        user = message.data.get('user', None)

        utterances = message.data.get('utterances', '')

        best_intent = None

        for utterance in utterances:
            try:
                # normalize() changes "it's a boy" to "it is boy"
                best_intent = next(self.engine.determine_intent(normalize(utterance, lang), 100))

                best_intent['utterance'] = utterance
            except StopIteration as e:
                logger.exception(e)
                continue

        if best_intent and best_intent.get('confidence', 0.0) > 0.0:
            best_intent['lang'] = lang
            best_intent['user'] = user

            reply = message.reply(best_intent.get('intent_type'), best_intent)
            self.emitter.emit(reply)
        elif len(utterances) == 1:
            self.emitter.emit(Message("intent_failure", {
                "utterance": utterances[0],
                "lang": lang
            }))
        else:
            self.emitter.emit(Message("multi_utterance_intent_failure", {
                "utterances": utterances,
                "lang": lang
            }))

    def handle_register_vocab(self, message):

        start_concept = message.data.get('start')
        end_concept = message.data.get('end')
        regex_str = message.data.get('regex')
        alias_of = message.data.get('alias_of')

        if regex_str:
            self.engine.register_regex_entity(regex_str)
        else:
            self.engine.register_entity(start_concept, end_concept, alias_of=alias_of)

    def handle_register_intent(self, message):
        intent = open_intent_envelope(message)
        self.engine.register_intent_parser(intent)

    def handle_detach_intent(self, message):
        intent_name = message.data.get('intent_name')
        new_parsers = [
            p for p in self.engine.intent_parsers if p.name != intent_name]
        self.engine.intent_parsers = new_parsers

    def handle_detach_skill(self, message):
        skill_name = message.data.get('skill_name')
        new_parsers = [
            p for p in self.engine.intent_parsers if
            not p.name.startswith(skill_name)]
        self.engine.intent_parsers = new_parsers
