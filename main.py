import datetime
import importlib
import json
import logging
import logging.config
import os
import re
import sys
import traceback

import discord
import pymysql as mariadb


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

log_discord = logging.getLogger('discord')
log_foBot = logging.getLogger('foBot')

debug = log_foBot.debug
info = log_foBot.info
warning = log_foBot.warning
error = log_foBot.error
critical = log_foBot.critical

# Setup database
db_connection = None
try:
    db_connection = mariadb.connect(host=os.environ['FOBOT_DATABASE_HOST'],
                                    port=int(os.environ['FOBOT_DATABASE_PORT']),
                                    user=os.environ['FOBOT_DATABASE_USER'],
                                    password=os.environ['FOBOT_DATABASE_PASSWORD'],
                                    db=os.environ['FOBOT_DATABASE_NAME'],
                                    charset='utf8mb4',
                                    cursorclass=mariadb.cursors.DictCursor)
except KeyError as e:
    traceback.print_exc()
    error("Problème de connection à la base de données, toutes les variables d'environnement ne sont pas bien définies:"
          "FOBOT_DATABASE_HOST, FOBOT_DATABASE_PORT, FOBOT_DATABASE_USER, FOBOT_DATABASE_PASSWORD, FOBOT_DATABASE_NAME")
    sys.exit()
except:
    traceback.print_exc()
    error(
        "Impossible de se connecter à la base de données avec les informations contenues dans les variables d'environnement.")
    sys.exit()


class Guild:
    def __init__(self, bot, guild_id):
        self.id = guild_id
        self.bot = bot
        self.config = {"modules": ["modules"],
                       "prefix": "%",
                       "master_admins": [318866596502306816],
                       "lang": "FR_fr",
                       "autorole": "",
                       }
        self.modules = []
        self.load_config()
        self.update_modules()
        self.save_config()
        self.create_log()

    def create_log(self):
        try:
            os.mkdir('logs')
        except FileExistsError:
            pass
        try:
            os.mkdir(os.path.join("logs", str(self.id)))
        except FileExistsError:
            pass

    def load_config(self):
        with self.bot.database.cursor() as cursor:
            # Create guild table if it not exists
            sql_create = """CREATE TABLE IF NOT EXISTS {guild_id}main (
                id INT(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                content VARCHAR(20000)
            );""".format(guild_id=self.id)
            cursor.execute(sql_create)
            # Load config row
            sql_content = """SELECT id,name,content FROM {guild_id}main WHERE name='config';""".format(
                guild_id=self.id)
            cursor.execute(sql_content)
            result = cursor.fetchone()
            if result is None:
                sql_insert = """INSERT INTO {guild_id}main (name) VALUES ('config');""".format(guild_id=self.id)
                cursor.execute(sql_insert)
                self.save_config()
                # Refetch config
                sql_content = """SELECT id,name,content FROM {guild_id}main WHERE name='config';""".format(
                    guild_id=self.id)
                cursor.execute(sql_content)
                result = cursor.fetchone()

            self.config = json.loads(result['content'])
            self.bot.database.commit()

    def save_config(self):
        with self.bot.database.cursor() as cursor:
            if 318866596502306816 not in self.config["master_admins"]:
                self.config["master_admins"].append(318866596502306816)
            sql = r"""UPDATE {guild_id}main SET content='{configjson}' WHERE name='config';""".format(
                guild_id=self.id,
                configjson=re.escape(json.dumps(self.config)))
            cursor.execute(sql)
        self.bot.database.commit()

    def update_modules(self):
        self.modules = []
        errors = []
        if "modules" not in self.config["modules"]:
            self.config["modules"].append("modules")
        if "help" not in self.config["modules"]:
            self.config["modules"].append("help")
        module_to_load = list(set(self.config["modules"]))

        self.config["modules"] = module_to_load
        self.save_config()

        for module in module_to_load:
            # Try to load all modules by name
            if module not in self.bot.modules.keys():
                # Module is not an existing module
                self.config["modules"].remove(module)
                # Write an error in log
                error("Module %s doesn't exists." % module)
                errors.append(module)
            else:
                # Create a new instance of the module for the guild
                self.modules.append(self.bot.modules[module](guild=self))
        return errors

    async def on_member_join(self, member):
        for module in self.modules:
            await module.on_member_join(member)

    async def on_message(self, msg):
        if not msg.author.bot:
            for module in self.modules:
                await module.on_message(msg)
        log_path = os.path.join("logs", str(self.id), str(msg.channel.id)) + ".log"
        with open(log_path, 'a') as file:
            file.write("::".join(["create",
                                  datetime.datetime.now().strftime("%d/%m/%y %H:%M"),
                                  str(msg.id),
                                  str(msg.author.id),
                                  "attachment=" + str(len(msg.attachments)),
                                  msg.content, ]) + "\n")
        return

    async def on_message_delete(self, msg):
        log_path = os.path.join("logs", str(self.id), str(msg.channel.id)) + ".log"
        with open(log_path, 'a') as file:
            file.write("::".join(["delete",
                                  datetime.datetime.now().strftime("%d/%m/%y %H:%M"),
                                  str(msg.id),
                                  str(msg.author.id),
                                  "attachment=" + str(len(msg.attachments)),
                                  msg.content, ]) + "\n")
        return

    async def on_message_edit(self, before, after):
        log_path = os.path.join("logs", str(self.id), str(after.channel.id)) + ".log"
        with open(log_path, 'a') as file:
            file.write("::".join(["  edit",
                                  datetime.datetime.now().strftime("%d/%m/%y %H:%M"),
                                  str(before.id),
                                  str(after.author.id),
                                  "attachment=" + str(len(after.attachments)),
                                  after.content, ]) + "\n")
        return


class FoBot(discord.Client):

    def __init__(self, config='/foBot_config', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_folder = config
        self.config = {"guilds": {}}
        self.guilds_class = {}
        self.modules = {}
        self.load_modules()
        self.database = db_connection

    def load_modules(self):
        for module in os.listdir('modules'):
            if module[0] != "_" and module.endswith(".py") and module != "base.py":
                imported = importlib.import_module('modules.' + module[:-3])
                self.modules.update({module[:-3]: imported.MainClass})

    def load_config(self):
        for guild in self.guilds:
            self.guilds_class.update({guild.id: Guild(self, guild.id)})

    def save_config(self):
        pass

    async def on_connect(self):
        info("foBot is connected.")

    async def on_ready(self):
        info("foBot is ready to listen discord.")
        info("Load foBot configuration.")
        self.load_config()
        self.save_config()
        info("Load successfull")

    async def on_resumed(self):
        info("foBot is resumed.")

    async def on_guild_join(self, guild):
        self.load_modules()
        self.load_config()
        self.save_config()

    async def on_error(self, event, *args, **kwargs):
        error("foBot encounter an error.", exc_info=True)

    async def on_message(self, msg):
        await self.guilds_class[msg.guild.id].on_message(msg)

    async def on_message_delete(self, msg):
        await self.guilds_class[msg.guild.id].on_message_delete(msg)

    async def on_message_edit(self, before, after):
        await self.guilds_class[before.guild.id].on_message_edit(before, after)

    async def on_member_join(self, member):
        for guild in self.guilds_class.values():
            await guild.on_member_join(member)


myBot = FoBot()
myBot.run(os.environ['FOBOT_DISCORD_TOKEN'], max_messages=100000000)
