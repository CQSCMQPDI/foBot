class MainClass:
    name = "pi"

    def __init__(self, guild):
        self.guild = guild

    async def pi(self, msg, command, args):
        pass

    async def pi_search(self, msg, command, args):
        pass

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "pi":
                self.pi(msg, command, args)
        return