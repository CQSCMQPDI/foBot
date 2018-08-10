import discord

class MainClass:
    name = "modules"
    description = "Permet de gérer les modules."

    def __init__(self, guild):
        self.guild = guild
        self.authorized = [318866596502306816]

    async def load(self, msg, command, args):
        if msg.author.id in self.authorized:
            errors = []
            for arg in args:
                if args not in self.guild.config["modules"]:
                    self.guild.config["modules"].append(args[0])
                    errors.extend(self.guild.update_modules())
            if errors:
                textes = [
                    ("Erreur lors de l'activation du module %s:" % module,
                     "Celui-ci n'existe pas. Tapez %slist_modules pour voir la liste des modules disponibles" %
                     self.guild.config["prefixe"])
                    for module in errors
                ]
                embed = discord.Embed(title="Erreur")
                for erreur in textes:
                    embed.add_field(name=erreur[0], value=erreur[1], inline=False)
                await msg.channel.send(embed=embed)
                self.guild.save_config()
        else:
            embed = discord.Embed(title="Erreur")
            if len(args) == 1:
                embed.add_field(name="Erreur lors du chargement du module.",
                                value="Vous n'avez pas la permission de charger un module.")
            else:
                embed.add_field(name="Erreur lors du chargement du module.",
                                value="Vous n'avez pas la permission de charger un module.")
            await msg.channel.send(embed=embed)

    async def list_modules(self, msg, command, args):
        embed = discord.Embed(title="Liste des modules")
        for module, classe in self.guild.bot.modules.items():
            if module not in self.guild.config["modules"]:
                embed.add_field(name=classe.name+":", value=classe.description, inline=False)
            else:
                embed.add_field(name="***"+classe.name + "***:", value=classe.description, inline=False)
        await msg.channel.send(embed=embed)

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefixe"]):
            command, *args = msg.content.lstrip(self.guild.config["prefixe"]).split(" ")
            print(command, args)
            if command == "load":
                await self.load(msg, command, args)
            elif command == "list_modules":
                await self.list_modules(msg, command, args)

