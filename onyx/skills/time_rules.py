#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

import abc
import re

__author__ = 'jdorleans'


class AbstractTimeRules(object):
    def __init__(self):
        self.rules = None
        self.init_rules()
        self.build_repeat_time_regex()
        self.build_time_regex()

    @abc.abstractmethod
    def init_rules(self):
        pass

    @abc.abstractmethod
    def build_repeat_time_regex(self):
        pass

    def build_time_regex(self):
        for idx, regex in enumerate(self.rules.get('time_regex')):
            regex = regex.replace('<time_advs>', self.rules.get('time_advs'))
            regex = regex.replace('<day_parts>', self.rules.get('day_parts'))
            regex = regex.replace('<time_units>', self.rules.get('time_units'))
            regex = regex.replace('<week_days>', self.rules.get('week_days'))
            regex = regex.replace('<months>', self.rules.get('months'))
            regex = regex.replace('<mealtimes>', self.rules.get('mealtimes'))
            regex = regex.replace(
                '<celebrations>', self.rules.get('celebrations'))
            regex = regex.replace(
                '<repeat_time_regex>', self.rules.get('repeat_time_regex'))
            self.rules.get('time_regex')[idx] = regex.lower()

    # days is an array starting from Monday (0) to Sunday (6)
    def get_week_days(self, sentence):
        days = None
        pattern = re.compile(
            self.rules.get('repeat_time_regex'), re.IGNORECASE)
        result = pattern.search(sentence)
        if result:
            group = result.group()
            if self.is_all_days(group):
                days = [True, True, True, True, True, True, True]
            else:
                days = [False, False, False, False, False, False, False]
                self.fill_week_days(group, days)
        return days

    @abc.abstractmethod
    def is_all_days(self, group):
        pass

    @abc.abstractmethod
    def fill_week_days(self, group, days):
        pass


class TimeRulesEnUs(AbstractTimeRules):
    def __init__(self):
        super(TimeRulesEnUs, self).__init__()

    def init_rules(self):
        self.rules = {
            'time_advs': 'today|tonight|tomorrow',
            'time_units': 'second|minute|hour|day|week|month|year',
            'day_parts': 'dawn|morning|noon|afternoon|evening|night|midnight',
            'week_days': (
                'monday|tuesday|wednesday|thursday|friday|saturday|sunday'),
            'months': (
                'january|february|march|april|may|june|july|august|september|'
                'october|november|december'),
            'mealtimes': (
                'breakfast|lunchtime|teatime|dinnertime|lunch time|tea time|'
                'dinner time'),
            'celebrations': 'easter|christmas',
            'repeat_time_regex': (
                '((every|each|all) (single )?(day|(<week_days>)s?( (and )?'
                '(<week_days>)s?)*))|daily|everyday'),
            'time_regex': [
                '(<time_advs>)',
                '((at|in the|during the|tomorrow)\s)?(<day_parts>)',
                '(in )?(a|an|one|two|\d+\.?\d*) (<time_units>)s?( later)?',
                'on (<week_days>)',
                '(on|the) (\d+(rd|st|nd|th)?\s)?(<months>)( the )?'
                '(\s\d+(rd|st|nd|th)?)?(\s?,?\s?\d*)?',
                'in (\d\d\d\d)', 'at (<mealtimes>|<celebrations>)',
                "(at|by) \d+((:| and )\d+)?( and a (quarter|half))?"
                "\s?((a\.?m\.?|p\.?m\.?)|o'clock)?",
                '(in |in the )?next (<time_units>|<day_parts>|<week_days>'
                '|<months>|<mealtimes>|<celebrations>)s?',
                '<repeat_time_regex>'
            ]
        }

    def build_repeat_time_regex(self):
        week_days = self.rules.get('week_days')
        repeat_time_regex = self.rules.get('repeat_time_regex')
        self.rules['repeat_time_regex'] = repeat_time_regex.replace(
            '<week_days>', week_days)

    def is_all_days(self, group):
        for d in [' day', 'daily', 'everyday']:
            if group.__contains__(d):
                return True
        return False

    def fill_week_days(self, group, days):
        if group.__contains__('monday'):
            days[0] = True
        if group.__contains__('tuesday'):
            days[1] = True
        if group.__contains__('wednesday'):
            days[2] = True
        if group.__contains__('thursday'):
            days[3] = True
        if group.__contains__('friday'):
            days[4] = True
        if group.__contains__('saturday'):
            days[5] = True
        if group.__contains__('sunday'):
            days[6] = True

class TimeRulesFrFr(AbstractTimeRules):
    def __init__(self):
        super(TimeRulesFrFr, self).__init__()

    def init_rules(self):
        self.rules = {
            'time_advs': "aujourd'hui|ce soir|demain",
            'time_units': 'seconde|minute|heure|jour|semaine|mois|année',
            'day_parts': 'aube|matin|midi|après-midi|soir|nuit|minuit',
            'week_days': (
                'lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche'),
            'months': (
                'janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|'
                'septembre|novembere|decembre'),
            'mealtimes': (
                'repas|manger|gouter|diner|dejeuner'),
            'celebrations': 'pâque|noël',
            'repeat_time_regex': (
                '((tous|chaque|tout) (les )?(jour|jours|(<week_days>)s?( (et )?'
                '(<week_days>)s?)*))|journalier|tous les jours'),
            'time_regex': [
                '(<time_advs>)',
                '((à|dans le|pendant|demain)\s)?(<day_parts>)',
                '(dans )?(un|une|deux|\d+\.?\d*) (<time_units>)s?( apres)?',
                'le? (<week_days>)',
                '(on|the) (\d+(rd|st|nd|th)?\s)?(<months>)( the )?'
                '(\s\d+(rd|st|nd|th)?)?(\s?,?\s?\d*)?',
                'dans (\d\d\d\d)', 'a (<mealtimes>|<celebrations>)',
                "(at|by) \d+((:| and )\d+)?( and a (quarter|half))?"
                "\s?((a\.?m\.?|p\.?m\.?)|o'clock)?",
                '(in |in the )?next (<time_units>|<day_parts>|<week_days>'
                '|<months>|<mealtimes>|<celebrations>)s?',
                '<repeat_time_regex>'
            ]
        }

    def build_repeat_time_regex(self):
        week_days = self.rules.get('week_days')
        repeat_time_regex = self.rules.get('repeat_time_regex')
        self.rules['repeat_time_regex'] = repeat_time_regex.replace(
            '<week_days>', week_days)

    def is_all_days(self, group):
        for d in [' jour', 'journalier', 'journalière', 'tous les jours']:
            if group.__contains__(d):
                return True
        return False

    def fill_week_days(self, group, days):
        if group.__contains__('lundi'):
            days[0] = True
        if group.__contains__('mardi'):
            days[1] = True
        if group.__contains__('mercredi'):
            days[2] = True
        if group.__contains__('jeudi'):
            days[3] = True
        if group.__contains__('vendredi'):
            days[4] = True
        if group.__contains__('samedi'):
            days[5] = True
        if group.__contains__('dimanche'):
            days[6] = True



KEY_MAP = {
    'fr-FR': TimeRulesFrFr,
    'en-US': TimeRulesEnUs,
}


def create(lang):
    clazz = KEY_MAP.get(lang)
    if not clazz:
        clazz = TimeRulesEnUs()
    return clazz()
