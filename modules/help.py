import discord
import traductions as tr


class MainClass:
    name = "modules"

    def __init__(self, guild):
        self.guild = guild

    async def help(self, msg, command, args):
        if len(args) == 0:
            texte = "Voici l'aide générale du bot:"
            for module in self.guild.config["modules"]:
                texte += "\n**"
                texte += module
                texte += "**: "
                texte += tr.tr[self.guild.config["lang"]]["modules"][module]["description"]
                texte += "\n\tCommandes: "
                texte += ", ".join(
                    [commande for commande in tr.tr[self.guild.config["lang"]]["modules"][module]["help"].keys()])
            await msg.channel.send(texte)
            return
        elif len(args[0].split(":")) == 1:
            if args[0] in tr.tr[self.guild.config["lang"]]["modules"].keys():
                texte = "Voici l'aide pour le module {module}:".format(module=args[0])
                for commande, aide in tr.tr[self.guild.config["lang"]]["modules"][args[0]]["help"].items():
                    texte += "\n**"
                    texte += commande
                    texte += "**: "
                    texte += aide["description"]
                await msg.channel.send(texte)
                return
            else:
                # module non existant
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["ModuleNotFoundError"]["text"]
                                       .format(prefix=self.guild.config["prefix"], module=args[0]))
                return
        elif len(args[0].split(":")) == 2:
            module, fonction = args[0].split(":")
            if module in tr.tr[self.guild.config["lang"]]["modules"].keys():
                if fonction in tr.tr[self.guild.config["lang"]]["modules"][module]["help"].keys():
                    texte = "Aide de la fonction {command}".format(command=fonction)
                    for exemple in tr.tr[self.guild.config["lang"]]["modules"][module]["help"][fonction]["examples"]:
                        texte += "\n"
                        texte += exemple[0].format(prefix=self.guild.config["prefix"])
                        texte += ": "
                        texte += exemple[1]
                    await msg.channel.send(texte)
                else:
                    await msg.channe.send(tr.tr[self.guild.config["lang"]]["errors"]["CommandNotFoundError"].format(command=fonction))
            else:
                # module non existant
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["ModuleNotFoundError"]["text"]
                                       .format(prefix=self.guild.config["prefix"], module=module))
            return

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "help":
                await self.help(msg, command, args)
        return
