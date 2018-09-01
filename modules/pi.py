import os
import traductions as tr


class MainClass:
    name = "pi"

    def __init__(self, guild):
        self.guild = guild
        self.pi_file = "D:\\Users\\louis chauvet\\Documents\\GitHub\\foBot\\modules\\pi\\pi1.txt"

    async def pi(self, msg, command, args):
        start = 0
        if len(args) == 1:
            try:
                start = int(args[0])
            except ValueError:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["Errors"]["TooBigNumberPiError"])
        with open(self.pi_file) as pi_file:
            pi_file.read(start)
            txt = pi_file.read(2000)
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["pi"]["pi"].format(debut=start))
            await msg.channel.send(txt)

    async def pi_search(self, msg, command, args):
        pass

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "pi":
                await self.pi(msg, command, args)
        return
