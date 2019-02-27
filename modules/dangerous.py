import traductions as tr
import sys


def to_str(entier):
    return str(entier).replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e") \
        .replace("6", "f").replace("7", "g").replace("8", "h").replace("9", "i").replace("0", "j")


def pp(cursor, data=None, rowlens=0):
    d = cursor.description
    if not d:
        return "#### NO RESULTS ###"
    names = []
    lengths = []
    rules = []
    if not data:
        data = cursor.fetchall()
    for dd in d:  # iterate over description
        l = dd[1]
        if not l:
            l = 12  # or default arg ...
        l = min(l, len(dd[0]))  # Handle long names
        names.append(dd[0])
        print(dd)
        lengths.append(l)
    for col in range(len(lengths)):
        if rowlens:
            rls = [len(row[col]) for row in data if row[col]]
            lengths[col] = max([lengths[col]] + rls)
        rules.append("-" * lengths[col])
    format = " ".join(["%%-%ss" % l for l in lengths])
    result = [format % tuple(names)]
    result.append(format % tuple(rules))
    for row in data:
        result.append(format % tuple([str(v) for v in row.values()]))
    return "\n".join(result)


from modules.base import MainClass as Base


class MainClass(Base):
    name = "dangerous"

    def __init__(self, guild):
        self.guild = guild

    async def restart(self, msg, command, args):
        exit()

    async def stop(self, msg, command, args):
        exit(44)

    async def execute(self, msg, command, args):
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return
        with self.guild.bot.database.cursor() as cursor:
            print(' '.join(args))
            cursor.execute(' '.join(args))
            self.guild.bot.database.commit()
            string = pp(cursor)
            for to_send in string.split("\n"):
                await msg.channel.send("```" + to_send + "```")

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"] * 2):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "execute":
                await self.execute(msg, command, args)
            elif command == "restart":
                await self.restart(msg, command, args)
            elif command == "stop":
                await self.stop(msg, command, args)
        return
