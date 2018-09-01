import ftplib
import importlib
import json
import logging
import logging.config
import os
import sys

import discord
from fs.dropboxfs import DropboxFS
from fs.osfs import OSFS
from fs import path

fileSystem = None

if os.environ.get("DROPBOX_ACCESS_TOKEN", False):
    print("FTP")
    fileSystem = DropboxFS(os.environ["DROPBOX_ACCESS_TOKEN"])
else:
    print("OS")
    fileSystem = OSFS(os.getcwd())


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


class Guild:
    def __init__(self, bot, guild_id, config_file):
        self.id = guild_id
        self.bot = bot
        self.config_file = config_file
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
        if self.bot.fileSystem.exists(self.config_file):
            try:
                # Loading configuration file
                with self.bot.fileSystem.open(self.config_file) as conf:
                    self.config.update(json.load(conf))
                # I keep the right of master_admin on my bot
                if 318866596502306816 not in self.config["master_admins"]:
                    self.config["master_admins"].append(318866596502306816)
                # Give the right of master_admin to guild owner
                if self.bot.get_guild(self.id) is not None:
                    if self.bot.get_guild(self.id).owner.id not in self.config["master_admins"]:
                        self.config["master_admins"].append(self.bot.get_guild(self.id).owner.id)
                self.save_config()

            except PermissionError:
                error("Cannot open config file for server %s." % self.id)

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

    def save_config(self):
        try:
            with self.bot.fileSystem.open(self.config_file, 'w') as conf_file:
                json.dump(self.config, conf_file)
        except PermissionError:
            error("Cannot write to configuration file.")

    async def on_message(self, msg):
        if not msg.author.bot:
            for module in self.modules:
                await module.on_message(msg)
        return


class FoBot(discord.Client):

    def __init__(self, config='/foBot_config', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_folder = config
        self.config = {"guilds": {}}
        self.guilds_class = {}
        self.modules = {}
        self.load_modules()
        self.fileSystem = fileSystem

    def load_modules(self):
        for module in os.listdir('modules'):
            if module != "__pycache__" and module.endswith(".py"):
                imported = importlib.import_module('modules.' + module[:-3])
                self.modules.update({module[:-3]: imported.MainClass})

    def load_config(self):
        if self.fileSystem.exists(path.join(self.config_folder, "conf.json")):
            try:
                # Loading configuration file
                with self.fileSystem.open(path.join(self.config_folder, "conf.json")) as conf:
                    self.config.update(json.load(conf))
            except PermissionError:
                critical("Cannot open config file.")
                sys.exit()
            info("Configuration for foBot loaded. Check for new guilds.")
            # Change all str key of guild into int ones
            guilds = {int(k): v for k, v in self.config["guilds"].items()}
            del self.config["guilds"]
            self.config.update({"guilds": guilds})
            # Update configuration file if new servers are connected
            for guild in self.guilds:
                if guild.id not in list(self.config["guilds"].keys()):
                    self.config["guilds"].update(
                        {guild.id: path.join(self.config_folder, str(guild.id) + ".json")})
            for guild_id, guild_config_file in self.config["guilds"].items():
                self.guilds_class.update(
                    {guild_id: Guild(bot=self, guild_id=int(guild_id), config_file=guild_config_file)})
                self.save_config()
        elif self.fileSystem.exists(self.config_folder):
            self.save_config()
        else:
            try:
                self.fileSystem.makedir(self.config_folder)
            except PermissionError:
                critical("Cannot create config folder.")
                sys.exit()

    def save_config(self):
        for guild in self.guilds_class.values():
            guild.save_config()
        try:
            with self.fileSystem.open(path.join(self.config_folder, "conf.json"), 'w') as conf_file:
                json.dump(self.config, conf_file, indent=4)
        except PermissionError:
            critical("Cannot write to configuration file.")
            sys.exit()

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
        if os.environ.get("DROPBOX_ACCESS_TOKEN", False):
            print("FTP")
            self.fileSystem = DropboxFS(os.environ["DROPBOX_ACCESS_TOKEN"])
        else:
            print("OS")
            self.fileSystem = OSFS(os.getcwd())

    async def on_message(self, msg):
        await self.guilds_class[msg.guild.id].on_message(msg)


myBot = FoBot()
myBot.run(os.environ.get("DISCORD_TOKEN", ""), max_messages=100000000)
