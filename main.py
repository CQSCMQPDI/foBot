import asyncio
import json
import logging
import logging.config
import tornado.ioloop
import tornado.web

from bot.fobot import FoBot
from web.server import FoWeb


import pymysql as mariadb

import os

# Setup database
db_connection = mariadb.connect(host='127.0.0.1',
                                port=3307,
                                user=os.environ['FOBOT_DATABASE_USER'],
                                password=os.environ['FOBOT_DATABASE_PASSWORD'],
                                db='fobot',
                                charset='utf8mb4',
                                cursorclass=mariadb.cursors.DictCursor)


def to_str(entier):
    return str(entier).replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e") \
        .replace("6", "f").replace("7", "g").replace("8", "h").replace("9", "i").replace("0", "j")


# json decoder for int keys
class Decoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        result = super().decode(s)  # result = super(Decoder, self).decode(s) for Python 2.x
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):
            try:
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


def setup_logging(default_path='log_config.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()






eventloop = asyncio.get_event_loop()

foBot = FoBot(db_connection=db_connection)

foWeb = FoWeb(bot=None, db=db_connection)

bot_app = foBot.start(os.environ['DISCORD_TOKEN'], max_messages=100000000)
bot_task = asyncio.ensure_future(bot_app)

foWeb.listen(port=8888)
web_task = foWeb.get_task()

eventloop.run_forever()
