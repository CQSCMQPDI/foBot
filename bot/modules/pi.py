import re

from bot import traductions as tr


class MainClass:
    name = "pi"

    def __init__(self, guild):
        self.guild = guild
        self.pi_file = "modules/pi/pi1.txt"
        self.piFileError = False


    async def pi(self, msg, command, args):
        if not self.piFileError:
            start = 0
            if len(args) == 1:
                try:
                    start = int(args[0])
                except ValueError:
                    await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["TooBigNumberPiError"])
                    return
            if start > 1000000-2000:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["TooBigNumberPiError"])
                return
            with open(self.pi_file) as pi_file:
                pi_file.read(start)
                txt = pi_file.read(2000)
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["pi"]["pi"].format(debut=start))
                await msg.channel.send(txt)
                return
        else:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PiFileError"])
            return

    async def pi_search(self, msg, command, args):
        if not self.piFileError:
            if len(args) == 0:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
                return
            try:
                to_search = re.compile(args[0])
                if "*" in args[0] or "+" in args[0]:
                    await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["ForbiddenRegexError"])
                    return
                elif len(args[0]) > 50:
                    await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["RegexTooLongError"])
            except re.error:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["RegexError"])
                return
            with open(self.pi_file) as pi_file:
                pi = pi_file.readline()
                results = to_search.finditer(pi)
                texts = []
                for result in results:
                    texts.append(
                        tr.tr[self.guild.config["lang"]]["modules"]["pi"]["fpi"].format(
                            debut=result.start(0),
                            before=pi[result.start(0) - 10:result.start(0)],
                            find=pi[result.start(0):result.end(0)],
                            after=pi[result.end(0):result.end(0) + 10]
                        ))
            if texts:
                for text in texts[:10]:
                    await msg.channel.send(text)
            else:
                await msg.channel.send("Pas de résultats")
        else:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PiFileError"])
            return

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "pi":
                await self.pi(msg, command, args)
            elif command == "fpi":
                await self.pi_search(msg, command, args)
        return
