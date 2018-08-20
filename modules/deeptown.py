import datetime

import discord
import traductions as tr
import modules.deeptownOptimizer.optimizer as optimizer


class MainClass:
    name = "deeptown"

    def __init__(self, guild):
        self.guild = guild
        self.optimizer = optimizer.Optimizer()

    async def best_place_mine(self, msg, command, args):
        if args[0] not in self.optimizer.mines["0"].keys():
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["error"]["OreNotFoundError"].format(ore=args[0]))
            return
        else:
            text = tr.tr[self.guild.config["lang"]]["modules"]["deeptown"].format(ore=args[0])
            i = 0
            for mine in self.optimizer.best_mines(args[0]):
                if i >= 10:
                    break
                if mine[0] == "0":
                    continue
                text += mine[0].center(3, " ")
                text += ": "
                text += str(mine[1][args[0]] * 100)
                text += "%\n"
                i += 1
            text += "```"
            await msg.channel.send(text)
            return
        return

    async def reload_optimizer(self, msg, command, args):
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return
        else:
            self.optimizer = optimizer.Optimizer()

    async def to_make(self, msg, command, args):
        if args[0] not in self.optimizer.items.keys():
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["ItemNotFound"].format(item=args[0]))
        try:
            quantity = int(args[1])
        except ValueError:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotIntError"].format(number=args[1]))
            return
        result = self.optimizer.to_make(args[0], quantity)
        time = datetime.timedelta(seconds=int(result["time"]))
        needed = ", ".join([str(quantity) + " " + name for name, quantity in result["needed"].items()])
        await msg.channel.send(
            tr.tr[self.guild.config["lang"]]["modules"]["deeptown"]["to_make"].format(time=time, quantity=quantity,
                                                                                      item=args[0], needed=needed,
                                                                                      value=result["value"]))

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "best_place_mine":
                await self.best_place_mine(msg, command, args)
            elif command == "reload_optimizer":
                await self.reload_optimizer(msg, command, args)
            elif command == "to_make":
                await self.to_make(msg, command, args)
        return
