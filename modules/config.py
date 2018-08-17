import discord
import traductions as tr


class MainClass:
    name = "config"

    def __init__(self, guild):
        self.guild = guild
        self.forbiddenConfig = ["modules", "master_admins", "lang"]

    async def lang(self, msg, command, args):
        # Non authorized user
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return
        else:
            # No args
            if len(args) == 0:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
                return
            # Unknown lang
            elif args[0] not in tr.tr.keys():
                await msg.channel.send(
                    tr.tr[self.guild.config["lang"]]["errors"]["LangNotFoundError"] \
                        .format(lang=args[0], prefix=self.guild.config["prefix"] * 2))
                return
            else:
                # Normal case
                self.guild.config["lang"] = args[0]
                self.guild.save_config()
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["config"]["lang"].format(lang=args[0]))
                return

    async def list_lang(self, msg, command, args):
        embed = discord.Embed(title=tr.tr[self.guild.config["lang"]]["modules"]["config"]["list_lang"]["title"])
        for lang in tr.tr.keys():
            if lang == self.guild.config["lang"]:
                embed.add_field(name="***" + lang + "***", value=tr.tr[lang]["description"])
            else:
                embed.add_field(name=lang, value=tr.tr[lang]["description"])
        await msg.channel.send(embed=embed)
        return

    async def set(self, msg, command, args):

        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return
        else:
            if args[0] not in self.guild.config.keys():
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["UnknownConfigError"])
                return
            elif args[0] in self.forbiddenConfig:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["ForbiddenConfigError"])
                return
            else:
                self.guild.config[args[0]] = args[1]

    async def list(self, msg, command, args):
        embed = discord.Embed(title=tr.tr[self.guild.config["lang"]]["modules"]["config"]["list"]["title"])
        for param, description in tr.tr[self.guild.config["lang"]]["modules"]["config"]["list"]["params"].items():
            embed.add_field(name=param, value=description)
        await msg.channel.send(embed=embed)

    async def add_master_admin(self, msg, command, args):
        # Non authorized user
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return
        else:
            if len(msg.mentions) == 0:
                await msg.send(tr.tr[self.guild.config["lang"]]["errors"]["NoMentionsError"])
                return
            else:
                for user in msg.mentions:
                    if user.id not in self.guild.config["master_admins"]:
                        self.guild.config["master_admins"].append(user.id)
                    await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["config"]["add_master_admin"]\
                                           .format(user=user.mention))
                self.guild.save_config()
                return

    async def del_master_admin(self, msg, command, args):
        # Non authorized user
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return
        else:
            if len(msg.mentions) == 0:
                await msg.send(tr.tr[self.guild.config["lang"]]["errors"]["NoMentionsError"])
                return
            else:
                for user in msg.mentions:
                    while user.id in self.guild.config["master_admins"]:
                        self.guild.config["master_admins"].remove(user.id)
                    await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["config"]["del_master_admin"] \
                                           .format(user=user.mention))
                self.guild.save_config()
                return

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"] * 2):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "lang":
                await self.lang(msg, command, args)
            elif command == "list_lang":
                await self.list_lang(msg, command, args)
            elif command == "set":
                await self.set(msg, command, args)
            elif command == "list":
                await self.list(msg, command, args)
            elif command == "add_master_admin":
                await self.add_master_admin(msg, command, args)
            elif command == "del_master_admin":
                await self.del_master_admin(msg, command, args)
        return
