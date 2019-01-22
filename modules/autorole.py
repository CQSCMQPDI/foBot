from discord import Guild

from modules.base import MainClass as Base
from traductions import tr


class MainClass(Base):
    name = "config"

    async def on_member_join(self, member):
        role = self.guild.bot.get_guild(self.guild.id).get_role(int(self.guild.config["autorole"]))
        await member.add_roles(role)
        return

    async def update_role_id(self, msg, command, args):
        if len(msg.role_mentions) == 0:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NoMentionsError"])
            return
        elif len(msg.role_mentions) != 1:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["error"]["NotEnoughParamError"])
            return
        role = msg.role_mentions[0]
        self.guild.config["autorole"] = str(role.id)
        self.guild.save_config()
        return

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]*2):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]*2).split(" ")
            if command == "update_role":
                await self.update_role_id(msg, command, args)