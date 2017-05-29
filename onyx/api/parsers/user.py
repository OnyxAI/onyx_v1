# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.parsers import Parser
from onyx.api.user import *
from onyx.api.assets import Json
import re

users = User()
json = Json()

class UserParser(Parser):

    def __init__(self):
        super(UserParser, self).__init__()
        json.json = users.get()
        self.users = json.decode()

    def parse(self):
        self.result = []
        self.remplaced_str = self.text
        for user in self.users:
            regex = r'(?i)' + re.escape(user['username'])
            search = re.search(regex, self.text)
            if search:
                self.result.append(user['id'])
                self.remplaced_str = self.remplaced_str.replace(search.group(), '%USER%')
        return json.encode({"status":"success", "remplaced_str":self.remplaced_str, "kwargs":self.result})
