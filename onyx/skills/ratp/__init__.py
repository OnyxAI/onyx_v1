# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import json, requests, urllib

from onyx.skills.core import OnyxSkill

baseurl = "http://api-ratp.pierre-grimaud.fr/v2/"
linetype = "bus"
line = "72"
station = "Lamballe-Ankara"
destination = "Hotel de Ville"

introText = "Le prochain bus est "

class RatpSkill(OnyxSkill):

    def __init__(self):
        super(RatpSkill, self).__init__(name="RatpSkill")

    def get_schedule(self):
        url = baseurl + linetype + "/" + line + "/stations/" + urllib.quote(station) + "/?destination=" + urllib.quote(destination)
        resp = requests.get(url=url)
        data = json.loads(resp.text)
        str = introText

        for dest in data["response"]["schedules"]:
            str+= " " + dest["message"].replace("mn", "minutes")
            str+= " " + dest["destination"]

        return str


def create():
    return RatpSkill()
