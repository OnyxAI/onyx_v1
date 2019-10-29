# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.api.exceptions import *
from onyx.api.assets import Json
from onyx.extensions import db
from onyx.core.models import *
from onyx.util import getLogger

json = Json()
logger = getLogger('Weather')

class Weather:

    def __init__(self):
        self.latitude = None
        self.longitude = None
        self.token = None

    def set_token(self):
        try:
            
            query = ConfigModel.Config.query.filter_by(config="weather_api").first()
            if query == None:
                add = ConfigModel.Config(config="weather_api", value=self.token)

                db.session.add(add)
                db.session.commit()
            else:
                query.value = self.token

                db.session.add(query)
                db.session.commit()

            logger.info('Setting token success')
            return json.encode({"status": "success"})
        except Exception as e:
            logger.error('Setting token error : ' + str(e))
            raise WeatherException(str(e))

    def get_daily(self):
        try:
            json.url = "https://api.darksky.net/forecast/{}/{},{}?units=si".format(self.token, self.latitude, self.longitude)
            result = json.decode_url()

            return result
        except Exception as e:
            logger.error('Getting weather error : ' + str(e))
            raise WeatherException(str(e))


    def get_temp_str(self):
        try:
            json.url = "https://api.darksky.net/forecast/{}/{},{}?units=si".format(self.token, self.latitude, self.longitude)
            result = json.decode_url()
            return str(round(result["currently"]["temperature"]))
        except Exception as e:
            logger.error('Getting weather error : ' + str(e))
            raise WeatherException(str(e))

    def get_img(self):
        try:
            json.url = "https://api.darksky.net/forecast/{}/{},{}?units=si".format(self.token, self.latitude, self.longitude)
            result = json.decode_url()
            if result["currently"]["icon"] == 'rain':
                url = "rain.png"
            elif result["currently"]["icon"] == 'clear-day':
                url = "clear.png"
            elif result["currently"]["icon"] == 'thunderstorm':
                url = "pikacloud.png"
            elif result["currently"]["icon"] == 'snow':
                url = "snowing.png"
            elif result["currently"]["icon"] == 'fog':
                url = "cloud1.png"
            elif result["currently"]["icon"] == 'cloudy':
                url = "cloud.png"
            elif result["currently"]["icon"] == 'wind':
                url = "windy.png"
            else:
                url = ""
            return url
        except Exception as e:
            logger.error('Getting weather error : ' + str(e))
            raise WeatherException(str(e))
