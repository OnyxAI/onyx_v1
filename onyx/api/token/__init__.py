# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.core.models import *
from onyx.extensions import db
from onyx.api.assets import Json
from onyx.api.exceptions import *
from onyx.util.log import getLogger
from flask_jwt_extended import create_access_token

import datetime

logger = getLogger('Token')
json = Json()


class Token:

    def __init__(self):
        self.id = None
        self.current_user = None
        self.name = None
        self.token = None

    def get(self):
        try:
            query = TokenModel.Token.query.all()
            tokens = []
            for fetch in query:
                token = {}
                token['id'] = fetch.id
                token['name'] = fetch.name
                token['token'] = fetch.token

                tokens.append(token)

            return json.encode(tokens)
        except Exception as e:
            logger.error('Getting token error : ' + str(e))
            raise GetException(str(e))

    def add(self):
        try:
            expires = datetime.timedelta(days=365)
            self.token = create_access_token(self.current_user, expires_delta=expires)

            query = TokenModel.Token(name=self.name, token=self.token)

            db.session.add(query)
            db.session.commit()
            
            logger.info('Token ' + query.name + ' added successfuly')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.info('Token add error : ' + str(e))
            raise TokenException(str(e))


    def delete(self):
        try:
            jti = self.token
            try:
                revoked_token = RevokedTokenModel.RevokedToken(jti = jti)
                revoked_token.add()
            except Exception as e:
                logger.error('Token delete error : ' + str(e))
                raise TokenException(str(e))
            
            query = TokenModel.Token.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()

            logger.info('Token ' + query.name + ' deleted successfuly')

            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Token delete error : ' + str(e))
            raise TokenException(str(e))
