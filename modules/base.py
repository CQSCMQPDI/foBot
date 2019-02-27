class MainClass:
    name = ""

    def __init__(self, guild):
        self.guild = guild

    async def on_message(self, msg):
        return

    async def on_member_join(self, member):
        return
    
    async def on_message_delete(self, msg):
        return
    
    async def on_message_edit(self, before, after):
        return
        
    async def on_typing(self, channel, member, when):
        return
    
    async def on_reaction_add(self, reaction, user):
        return
    
    async def on_reaction_remove(self, reaction, user):
        return
    
    async def on_reaction_clean(self, message, reactions):
        return
