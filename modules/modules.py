import discord
import traductions as tr


class MainClass:
    name = "modules"

    def __init__(self, guild):
        self.guild = guild

    async def load(self, msg, command, args):
        if msg.author.id in self.guild.config["master_admin"]:
            errors = []
            for arg in args:
                if args not in self.guild.config["modules"]:
                    self.guild.config["modules"].append(arg)
                    errors.extend(self.guild.update_modules())
            if errors:
                texts = [
                    (tr.tr[self.guild.config["lang"]]["modules"]["modules"]["load"]["error"]["name"] % module,
                     tr.tr[self.guild.config["lang"]]["modules"]["modules"]["load"]["error"]["value"] %
                     self.guild.config["prefixe"])
                    for module in errors
                ]
                embed = discord.Embed(
                    title=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["load"]["error"]["title"])
                for error in texts:
                    embed.add_field(name=error[0], value=error[1], inline=False)
                await msg.channel.send(embed=embed)
                self.guild.save_config()
        else:
            embed = discord.Embed(
                title=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["load"]["permissionError"]["title"])
            if len(args) == 1:
                embed.add_field(
                    name=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["load"]["permissionError"]["one"][
                        "name"],
                    value=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["load"]["permissionError"]["one"][
                        "value"])
            else:
                embed.add_field(
                    name=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["load"]["permissionError"]["many"][
                        "name"],
                    value=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["load"]["permissionError"]["many"][
                        "value"])
            await msg.channel.send(embed=embed)
        return

    async def unload(self, msg, command, args):
        if msg.author.id in self.guild.config["master_admin"]:
            errors = []
            for arg in args:
                try:
                    self.guild.config["modules"].remove(arg)
                except ValueError:
                    errors.append(arg)

            errors.extend(self.guild.update_modules())
            if errors:
                textes = [
                    (tr.tr[self.guild.config["lang"]]["modules"]["modules"]["unload"]["error"]["name"] % module,
                     tr.tr[self.guild.config["lang"]]["modules"]["modules"]["unload"]["error"]["value"] %
                     self.guild.config["prefixe"])
                    for module in errors
                ]
                embed = discord.Embed(
                    title=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["unload"]["error"]["title"])
                for erreur in textes:
                    embed.add_field(name=erreur[0], value=erreur[1], inline=False)
                await msg.channel.send(embed=embed)
            self.guild.save_config()
        else:
            embed = discord.Embed(
                title=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["unload"]["permissionError"][
                    "title"])
            if len(args) == 1:
                embed.add_field(
                    name=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["unload"]["permissionError"]["one"][
                        "name"],
                    value=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["unload"]["permissionError"]["one"][
                        "value"])
            else:
                embed.add_field(
                    name=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["unload"]["permissionError"]["many"][
                        "name"],
                    value=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["unload"]["permissionError"]["many"][
                        "value"])
            await msg.channel.send(embed=embed)
        return

    async def list_modules(self, msg, command, args):
        embed = discord.Embed(title=tr.tr[self.guild.config["lang"]]["modules"]["modules"]["list_modules"]["title"])
        for module, classe in self.guild.bot.modules.items():
            if module not in self.guild.config["modules"]:
                embed.add_field(name=classe.name + ":",
                                value=tr.tr[self.guild.config["lang"]]["modules"][classe.name]["description"],
                                inline=False)
            else:
                embed.add_field(name="***" + classe.name + "***:",
                                value=tr.tr[self.guild.config["lang"]]["modules"][classe.name]["description"],
                                inline=False)
        await msg.channel.send(embed=embed)
        return

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefixe"]):
            command, *args = msg.content.lstrip(self.guild.config["prefixe"]).split(" ")
            if command == "load":
                await self.load(msg, command, args)
            elif command == "list_modules":
                await self.list_modules(msg, command, args)
            elif command == "unload":
                await self.unload(msg, command, args)
        return
