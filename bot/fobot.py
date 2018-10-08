import importlib
import json
import os
import re
import logging

import discord

log_discord = logging.getLogger('discord')
log_foBot = logging.getLogger('foBot')

debug = log_foBot.debug
info = log_foBot.info
warning = log_foBot.warning
error = log_foBot.error
critical = log_foBot.critical


def to_str(entier):
    return str(entier).replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e") \
        .replace("6", "f").replace("7", "g").replace("8", "h").replace("9", "i").replace("0", "j")


class Guild:
    def __init__(self, bot, guild_id):
        self.id = guild_id
        self.bot = bot
        self.config = {"modules": ["modules"],
                       "prefix": "§",
                       "master_admins": [318866596502306816],
                       "lang": "FR_fr"
                       }
        self.modules = []
        self.load_config()
        self.update_modules()
        self.save_config()

    def load_config(self):
        with self.bot.database.cursor() as cursor:
            # Create guild table if it not exists
            sql_create = """CREATE TABLE IF NOT EXISTS {guild_id} (
                id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                name varchar(50) NOT NULL,
                content JSON CHECK (JSON_VALID(content))
            );""".format(guild_id=to_str(self.id))
            cursor.execute(sql_create)
            # Load config row
            sql_content = """SELECT id,name,content FROM {guild_id} WHERE name='config';""".format(
                guild_id=to_str(self.id))
            cursor.execute(sql_content)
            result = cursor.fetchone()
            if result is None:
                sql_insert = """INSERT INTO {guild_id} (name) VALUES ('config');""".format(guild_id=to_str(self.id))
                cursor.execute(sql_insert)
                self.save_config()
                # Refetch config
                sql_content = """SELECT id,name,content FROM {guild_id} WHERE name='config';""".format(
                    guild_id=to_str(self.id))
                cursor.execute(sql_content)
                result = cursor.fetchone()

            self.config = json.loads(result['content'])
            self.bot.database.commit()

    def save_config(self):
        with self.bot.database.cursor() as cursor:
            sql = r"""UPDATE {guild_id} SET content='{configjson}' WHERE name='config';""".format(
                guild_id=to_str(self.id),
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

    async def on_message(self, msg):
        if not msg.author.bot:
            for module in self.modules:
                await module.on_message(msg)
            print(msg.author, msg.content)
        return


class FoBot(discord.Client):

    def __init__(self, config='/foBot_config', db_connection=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_folder = config
        self.config = {"guilds": {}}
        self.guilds_class = {}
        self.modules = {}
        self.load_modules()
        self.database = db_connection

    def load_modules(self):
        for module in os.listdir(os.path.join("bot", 'modules')):
            if module != "__pycache__" and module.endswith(".py"):
                imported = importlib.import_module('bot.modules.' + module[:-3])
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
