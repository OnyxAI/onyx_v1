# -*- coding: utf-8 -*-
"""
Onyx Project
https://onyxlabs.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
import tornado.ioloop as ioloop
import tornado.web as web
import os

from onyx.sockyx.service.ws import WebsocketEventHandler
from onyx.util import validate_param
from onyx.config import get_config

settings = {
    'debug': True
}

def main():
    import tornado.options
    
    tornado.options.parse_command_line()
    config = get_config('onyx')

    host = config.get("Websocket", "host")
    port = int(config.get("Websocket", "port"))
    route = config.get("Websocket", "route")
    validate_param(host, "websocket.host")
    validate_param(port, "websocket.port")
    validate_param(route, "websocket.route")

    routes = [
        (route, WebsocketEventHandler)
    ]
    application = web.Application(routes, **settings)
    application.listen(port, host)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
