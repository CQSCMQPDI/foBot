import importlib
import json
import logging
import logging.config
import os
import sys

import discord


def setup_logging(default_path='log_config.json', default_level=logging.INFO, env_key='LOG_CFG', sms=True):
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


class Guild():
    def __init__(self, bot, guild_id, config_file):
        self.id = guild_id
        self.bot = bot
        self.config_file = config_file
        self.config = {"modules": ["modules"],
                       "prefixe": "!",
                       }
        self.modules = []
        self.load_config()
        self.update_modules()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                # Loading configuration file
                with open(self.config_file) as conf:
                    self.config.update(json.load(conf))
            except PermissionError:
                error("Cannot open config file for server %s." % self.guild_id)

    def update_modules(self):
        self.modules = []
        errors = []
        for module in self.config["modules"]:
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
            with open(self.config_file, 'w') as conf_file:
                json.dump(self.config, conf_file)
        except PermissionError:
            error("Cannot write to configuration file.")

    async def on_message(self, msg):
        for module in self.modules:
            await module.on_message(msg)


class FoBot(discord.Client):

    def __init__(self, config='foBot_config', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_folder = config
        self.config = {"guilds": {}}
        self.guilds_class = {}
        self.modules = {}
        self.load_modules()

    def load_modules(self):
        for module in os.listdir('modules'):
            if module != "__pycache__":
                imported = importlib.import_module('modules.'+module[:-3])
                self.modules.update({module[:-3]:imported.MainClass})


    def load_config(self):
        if os.path.exists(os.path.join(self.config_folder, "conf.json")):
            try:
                # Loading configuration file
                with open(os.path.join(self.config_folder, "conf.json")) as conf:
                    self.config.update(json.load(conf))
            except PermissionError:
                critical("Cannot open config file.")
                sys.exit()
            info("Configuration for foBot loaded. Check for new guilds.")
            # Update configuration file if new servers are connected
            for guild in self.guilds:
                if str(guild.id) not in list(self.config["guilds"].keys()):
                    self.config["guilds"].update(
                        {str(guild.id): os.path.join(self.config_folder, str(guild.id) + ".json")})
            for guild_id, guild_config_file in self.config["guilds"].items():
                self.guilds_class.update({guild_id:Guild(bot=self, guild_id=guild_id, config_file=guild_config_file)})
        elif os.path.exists(self.config_folder):
            self.save_config()
        else:
            try:
                os.mkdir(self.config_folder)
            except PermissionError:
                critical("Cannot create config folder.")
                sys.exit()

    def save_config(self):
        for guild in self.guilds_class.values():
            guild.save_config()
        try:
            with open(os.path.join(self.config_folder, "conf.json"), 'w') as conf_file:
                json.dump(self.config, conf_file)
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

    async def on_error(self, event, *args, **kwargs):
        error("foBot encounter an error.", exc_info=True)

    async def on_message(self, msg):
        await self.guilds_class[str(msg.guild.id)].on_message(msg)


myBot = FoBot()
myBot.run("You bot token", max_messages=100000000)
