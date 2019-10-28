# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani   
"""

from onyx.util.lang.parse_en import *

from onyx.util.lang.parse_fr import extractnumber_fr
from onyx.util.lang.parse_fr import extract_numbers_fr
from onyx.util.lang.parse_fr import extract_datetime_fr
from onyx.util.lang.parse_fr import normalize_fr

from datetime import datetime
from dateutil.tz import gettz, tzlocal

from .log import getLogger

LOG = getLogger(__name__)



def extract_numbers(text, short_scale=True, ordinals=False, lang="en-US"):
    """
        Takes in a string and extracts a list of numbers.
    """
    lang_lower = str(lang).lower()
    if lang_lower.startswith("en"):
        return extract_numbers_en(text, short_scale, ordinals)
    elif lang_lower.startswith("fr"):
        return extract_numbers_fr(text, short_scale, ordinals)

    return []


def extract_number(text, short_scale=True, ordinals=False, lang="en-US"):
    """
        Takes in a string and extracts a number.
    """
    lang_lower = str(lang).lower()
    if lang_lower.startswith("en"):
        return extractnumber_en(text, short_scale=short_scale, ordinals=ordinals)
    elif lang_lower.startswith("fr"):
        return extractnumber_fr(text)

    return text


def extract_duration(text, lang="en-US"):
    """ 
        Convert an english phrase into a number of seconds
    """
    lang_lower = str(lang).lower()

    if lang_lower.startswith("en"):
        return extract_duration_en(text)

    return None


def extract_datetime(text, anchorDate=None, lang="en-US", default_time=None):
    """
        Extracts date and time information from a sentence.  Parses many of the
        common ways that humans express dates and times, including relative dates
        like "5 days from today", "tomorrow', and "Tuesday".
    """

    lang_lower = str(lang).lower()

    if not anchorDate:
        anchorDate = datetime.now()

    if lang_lower.startswith("en"):
        return extract_datetime_en(text, anchorDate, default_time)
    elif lang_lower.startswith("fr"):
        return extract_datetime_fr(text, anchorDate, default_time)


    return text


def normalize(text, lang="en-US", remove_articles=True):
    """
        Prepare a string for parsing
    """

    lang_lower = str(lang).lower()

    if lang_lower.startswith("en"):
        return normalize_en(text, remove_articles)
    elif lang_lower.startswith("fr"):
        return normalize_fr(text, remove_articles)

    return text

