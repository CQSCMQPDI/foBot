import random

from bot import traductions as tr
import json


def to_str(entier):
    return str(entier).replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e") \
        .replace("6", "f").replace("7", "g").replace("8", "h").replace("9", "i").replace("0", "j")


class MainClass:
    name = "avalon"

    def __init__(self, guild):
        self.guild = guild
        # Init database
        self.curent_games = []
        self.current_waiting_players = []
        self.current_roles = []
        self.current_players = []
        with self.guild.bot.database.cursor() as cursor:
            sql_init = "CREATE TABLE IF NOT EXISTS {guild_id}avalon (" \
                       "    id int(5) NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                       "    nb_joueurs int(5) NOT NULL," \
                       "    gentil_a   varchar(50) NOT NULL," \
                       "    gentil_b   varchar(50) NOT NULL," \
                       "    gentil_c   varchar(50)," \
                       "    gentil_d   varchar(50)," \
                       "    gentil_e   varchar(50)," \
                       "    gentil_f   varchar(50)," \
                       "    mechant_a  varchar(50) NOT NULL," \
                       "    mechant_b  varchar(50)," \
                       "    mechant_c  varchar(50)," \
                       "    mechant_d  varchar(50)," \
                       "    merlin     varchar(50) NOT NULL," \
                       "    assassin   varchar(50) NOT NULL," \
                       "    mordred    varchar(50)," \
                       "    perceval   varchar(50)," \
                       "    morgane    varchar(50)," \
                       "    oberon     varchar(50)," \
                       "    vainqueur  varchar(50)" \
                       ")".format(guild_id=self.guild.id)
            cursor.execute(sql_init)

    async def start(self, msg, command, args):
        if len(self.current_waiting_players) >= 5:
            await msg.channel.send(
                tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonstart"]["notenoughtplayers"])
            return
        elif len(self.current_waiting_players) != len(self.current_roles):
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonstart"]["rolesnotmatch"])
            return
        else:
            self.current_games.append({
                "channel": msg.channel.id,
                "players": self.current_waiting_players,
                "gentils": [],
                "mechants": [],
                "merlin": None,
                "assassin": None,
                "mordred": None,
                "perceval": None,
                "morgane": None,
                "oberon": None
            })
            for player in self.current_waiting_players:
                role = random.choose(self.current_roles)
                self.current_roles.remove()
            self.current_waiting_players = []

    async def quit(self, msg, command, args):
        if msg.author.id in self.current_waiting_players:
            self.current_waiting_players.remove(msg.author.id)
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonquit"]["quit"]
                                   .format(player_id=msg.author.id,
                                           nb_players=len(self.current_waiting_players)))
        elif msg.author.id in self.current_players:
            self.quitting_players.append(msg.author.id)
            to_del = []
            # Verify if everyone want to quit game
            for game in self.curent_games:
                stop_game = True
                for game_player in game.players:
                    if game_player not in self.quitting_player:
                        stop_game = False
                if stop_game:
                    to_del.append(game)
            for game in to_del:
                self.curent_games.remove(game)
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonquit"]["alreadyplaying"]
                                   .format(player_id=msg.authpr.id))

    async def join(self, msg, command, args):
        # Personne pas déjà en train d'attendre, ni en train de jouer
        if msg.author.id not in self.current_waiting_players + self.current_players:
            self.current_waiting_players.append(msg.author.id)
            await msg.channel.send(
                tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonjoin"]["join"]
                    .format(player_id=msg.author.id,
                            nb_players=len(self.current_waiting_players)))
            if len(self.current_waiting_players) >= 5:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonjoin"]["canplay"]
                                       .format(prefix=self.guild.config["prefix"]))
        elif msg.author.id in self.current_players:
            await msg.channel.send(
                tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonjoin"]["alreadyplaying"]
                    .format(player_id=msg.author.id))
        elif msg.author.id in self.current_waiting_players:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonjoin"]["alreadywaiting"]
                                   .format(player_id=msg.author.id))

    async def stats(self, msg, command, args):
        with self.guild.bot.database.cursor() as cursor:
            cursor.execute("SELECT id,nb_joueurs,vainqueur FROM {guild_id}avalon;".format(guild_id=self.guild.id))
            results = cursor.fetchall()
        nb_games = len(results)
        nb_victoire_gentil = len(list([result for result in results if results["vainqueur"] == "gentil"]))
        nb_victoire_mechant = nb_games - nb_victoire_gentil
        await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["avalon"]["avalonstats"]
                               .format(nb_games=nb_games,
                                       nb_victoire_gentil=nb_victoire_gentil,
                                       nb_victoire_mechant=nb_victoire_mechant))

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "avalonstats":
                await self.stats(msg, command, args)
            elif command == "avalonjoin":
                await self.join(msg, command, args)
            elif command == "avalonquit":
                await self.quit(msg, command, args)
        return
