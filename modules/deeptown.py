import datetime

import modules.deeptownOptimizer.optimizer as optimizer
import traductions as tr

item_type_priority = {
    "quest": 00,
    "crafted": 50,
    "chemical": 60,
    'organic': 70,
    "raw": 100,
}

from modules.base import MainClass as Base


class MainClass(Base):
    name = "deeptown"

    def __init__(self, guild):
        self.guild = guild
        self.optimizer = optimizer.Optimizer()

    async def reload_data(self, msg, command, args):
        pass

    async def best_place_mine(self, msg, command, args):
        if len(args) == 0:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
            return
        if args[0] not in self.optimizer.mines["0"].keys():
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["OreNotFoundError"].format(ore=args[0]))
            return
        else:
            text = tr.tr[self.guild.config["lang"]]["modules"]["deeptown"]["best_place_mine"].format(ore=args[0])
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
        if len(args) == 0:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
            return
        if args[0] not in self.optimizer.items.keys():
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["ItemNotFoundError"].format(item=args[0]))
            return
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

    async def to_make_recursive(self, msg, command, args):
        if len(args) == 0:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
            return
        if len(args) == 1:
            args.append("1")
        if args[0] not in self.optimizer.items.keys():
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["ItemNotFoundError"].format(item=args[0]))
            return
        try:
            quantity = int(args[1])
        except ValueError:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotIntError"].format(number=args[1]))
            return
        needed = self.optimizer.recursive_to_make(args[0], quantity)
        texte = tr.tr[self.guild.config["lang"]]["modules"]["deeptown"]["recursive_to_make"]["header"] \
            .format(item=args[0], quantity=quantity)
        needed.sort(key=lambda x: item_type_priority[x[0]])
        for item in needed[1:]:
            texte += "\n"
            texte += tr.tr[self.guild.config["lang"]]["modules"]["deeptown"]["recursive_to_make"]["line"] \
                .format(item=item[1], quantity=item[2], time=datetime.timedelta(seconds=int(item[3])))
        texte += "```"
        await msg.channel.send(texte)

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "best_place_mine":
                await self.best_place_mine(msg, command, args)
            elif command == "reload_optimizer":
                await self.reload_optimizer(msg, command, args)
            elif command == "to_make":
                await self.to_make(msg, command, args)
            elif command == "to_make_recursive":
                await self.to_make_recursive(msg, command, args)
        return
