import traductions as tr

from modules.base import MainClass as Base


class MainClass(Base):
    name = "github"

    def __init__(self, guild):
        self.guild = guild

    async def sourcecode(self, msg, command, args):
        await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["github"]["sourcecode"])

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "sourcecode":
                await self.sourcecode(msg, command, args)
        return
