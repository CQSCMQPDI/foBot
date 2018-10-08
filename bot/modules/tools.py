import time

import discord
from bot import traductions as tr


class MainClass:
    name = "tools"

    def __init__(self, guild):
        self.guild = guild

    async def ping(self, msg, command, args):

        embed = discord.Embed(title=tr.tr[self.guild.config["lang"]]["modules"]["tools"]["ping"]["title"])
        t1 = time.time()
        reponse = await msg.channel.send(embed=embed)
        for i in range(1, 5):
            embed = discord.Embed(title=tr.tr[self.guild.config["lang"]]["modules"]["tools"]["ping"]["title"])

            embed.add_field(name="Temps de réponse", value=str((time.time() - t1) / i) + "s  ")
            embed.add_field(name="Latence", value=str(self.guild.bot.latency))
            await reponse.edit(embed=embed)

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "ping":
                await self.ping(msg, command, args)
        return
