import os
import time

import discord

import traductions as tr


def to_str(entier):
    return str(entier).replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e") \
        .replace("6", "f").replace("7", "g").replace("8", "h").replace("9", "i").replace("0", "j")


from modules.base import MainClass as Base


class MainClass(Base):
    name = "survey"

    def __init__(self, guild):
        self.guild = guild
        self.current_surveys = {}
        self.create_table()

    def create_table(self):
        with self.guild.bot.database.cursor() as cursor:
            create_survey_table_sql = "CREATE TABLE IF NOT EXISTS {guild_id}surveys (" \
                                      "    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                      "    title VARCHAR(2000) NOT NULL," \
                                      "    depart BIGINT," \
                                      "    duree BIGINT" \
                                      ");".format(guild_id=self.guild.id)
            create_choices_table_sql = "CREATE TABLE IF NOT EXISTS {guild_id}survey_choices (" \
                                       "    id int(20) NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                       "    survey int(20) NOT NULL," \
                                       "    content VARCHAR(1000)," \
                                       "    attachment BLOB(67108864)," \
                                       "    attachment_name VARCHAR(1000)" \
                                       ");".format(guild_id=self.guild.id)
            create_vote_table_sql = "CREATE TABLE IF NOT EXISTS {guild_id}survey_votes (" \
                                    "    id int NOT NULL AUTO_INCREMENT PRIMARY KEY," \
                                    "    choice BIGINT NOT NULL," \
                                    "    user_id VARCHAR(20) NOT NULL" \
                                    ");".format(guild_id=self.guild.id)
            cursor.execute(create_choices_table_sql)
            cursor.execute(create_survey_table_sql)
            cursor.execute(create_vote_table_sql)
            self.guild.bot.database.commit()

    async def vote(self, msg, command, args):
        try:
            await msg.delete()
        except discord.Forbidden:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["DiscordForbiddenError"])
        if len(args) != 1:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
            return
        try:
            id_vote = int(args[0])
        except ValueError:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotANumberError"])
            return

        with self.guild.bot.database.cursor() as cursor:
            # récupération de l'id du sondage
            select_choice_sql = "SELECT survey FROM `{guild_id}survey_choices` WHERE id = %s;".format(
                guild_id=self.guild.id)
            cursor.execute(select_choice_sql, (id_vote))
            survey_id = [r["survey"] for r in cursor.fetchall()]

        if len(survey_id) == 0:  # Le choix n'existe pas
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["SurveyNotExistsError"])
            return

        with self.guild.bot.database.cursor() as cursor:
            # Récupération de la date de fin du sondage
            select_survey_sql = "SELECT depart, duree FROM `{guild_id}surveys` WHERE id=%s;".format(
                guild_id=self.guild.id)
            cursor.execute(select_survey_sql, (survey_id))
            r = cursor.fetchone()
            if r["depart"] is not None:
                fin = r["depart"] + r["duree"]
            else:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotYetPostedError"])
                return
            # Liste des précédents votes
            select_prec_votes_sql = "SELECT choice FROM `{guild_id}survey_votes` WHERE user_id=%s;".format(
                guild_id=self.guild.id)
            cursor.execute(select_prec_votes_sql, (msg.author.id))
            list_votes = [r["choice"] for r in cursor.fetchall()]
            # Liste des précédents sondages votés
            list_surveys_sql = "SELECT survey FROM `{guild_id}survey_choices` WHERE id=%s".format(
                guild_id=self.guild.id)
            list_surveys = []
            for id_choice in list_votes:
                cursor.execute(list_surveys_sql, (id_choice))
                list_surveys.append(cursor.fetchone()["survey"])

        if fin < time.time():  # Sondage terminé
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["SurveyCompletedError"])
            return
        if survey_id[0] in list_surveys:  # Déjà voté
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["AlreadyVote"])
            return

        # On peu voter, on insère dans la bdd
        with self.guild.bot.database.cursor() as cursor:
            sql_insert = "INSERT INTO `{guild_id}survey_votes` (choice, user_id) VALUES (%s, %s);" \
                .format(guild_id=self.guild.id)
            cursor.execute(sql_insert, (id_vote, msg.author.id))
        self.guild.bot.database.commit()
        await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["survey"]["vote"]
                               .format(id_auteur=msg.author.id))

    async def add_choice(self, msg, command, args):
        # L'utilisateur est un administrateur du bot
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return
        # Vérification du nombre de paramètres
        if len(args) < 2 or (len(args) < 1 and len(msg.attachments) < 1):
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
            return

        try:  # Tentative de conversion en nombre
            survey_id = int(args[0])
        except ValueError:
            msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotANumberError"])
            return

        # Vérification de l'existance du sondage
        with self.guild.bot.database.cursor() as cursor:
            sql_id = "SELECT id FROM `{guild_id}surveys`".format(guild_id=self.guild.id)
            cursor.execute(sql_id, ())
            liste_id = [r["id"] for r in cursor.fetchall()]

        if survey_id not in liste_id:  # Le sondage n'existe pas
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["SurveyNotExistsError"])
            return

            # Verification que le sondage n'a pas déjà été publié
            with self.guild.bot.database.cursor() as cursor:
                sql_depart = "SELECT depart FROM `{guild_id}surveys` WHERE id = %s".format(guild_id=self.guild.id)
                cursor.execute(sql_depart, (survey_id))
                depart = cursor.fetchone()["depart"]
            if depart is not None:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["AlreadySendSurvey"])
                return

        content = " ".join(args[1:])
        # Ecriture du fichier temporaire
        with open("temp_attachement" + str(survey_id), "w") as temp_file:
            temp_file.write("")
        file_name = ""
        # Si un fichier est présent dans le message on le sauvegarde
        if len(msg.attachments) > 0:
            attachment = msg.attachments[0]
            if attachment.size > 67108864:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["AttachementTooBigError"])
                return
            with open("temp_attachement" + str(survey_id), "wb") as temp_file:
                await attachment.save(temp_file)
            file_name = attachment.filename
        # On insère le choix dans la base de données
        with self.guild.bot.database.cursor() as cursor:
            sql_insert = "INSERT INTO `{guild_id}survey_choices`  (survey, content, attachment, attachment_name) VALUES (%s, %s, %s, %s)".format(
                guild_id=self.guild.id)
            with open("temp_attachement" + str(survey_id), "rb") as temp_file:
                cursor.execute(sql_insert, (survey_id, content, temp_file.read(), file_name))
        os.remove("temp_attachement" + str(survey_id))
        self.guild.bot.database.commit()

    async def create_survey(self, msg, command, args):
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return

        if len(args) < 2:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
            return
        else:
            date_str = args[0]
            content = " ".join(args[1:])

            day_split = date_str.split("d")
            if len(day_split) == 1 and "d" not in date_str:
                jours = "0"
                next_split = date_str
            elif "d" in date_str and day_split[1] == "":
                jours = day_split[0]
                next_split = "0h0m0s"
            else:
                jours = day_split[0]
                next_split = day_split[1]

            hour_split = next_split.split("h")
            if len(hour_split) == 1 and "h" not in date_str:
                heures = "0"
                next_split = date_str
            elif "h" in date_str and hour_split[1] == "":
                heures = hour_split[0]
                next_split = "0m0s"
            else:
                heures = hour_split[0]
                next_split = hour_split[1]

            minute_split = next_split.split("m")
            if len(minute_split) == 1 and "h" not in date_str:
                minutes = "0"
                next_split = date_str
            elif "m" in date_str and minute_split[1] == "":
                minutes = minute_split[0]
                next_split = "0s"
            else:
                minutes = minute_split[0]
                next_split = minute_split[1]

            second_split = next_split.split("s")
            if len(second_split) == 1 and "s" not in date_str:
                secondes = "0"
            else:
                secondes = second_split[0]

            try:
                jours = int(jours)
                heures = int(heures)
                minutes = int(minutes)
                secondes = int(secondes)
            except ValueError:
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotANumberError"])
                return

            total = jours * 24 * 60 * 60 + heures * 60 * 60 + minutes * 60 + secondes  # Durée du sondage

            with self.guild.bot.database.cursor() as cursor:
                insert_sql = "INSERT INTO `{guild_id}surveys` (title, duree) VALUES (%s, %s);".format(
                    guild_id=self.guild.id)
                cursor.execute(insert_sql, (content, total))
                self.guild.bot.database.commit()
                await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["survey"]["create_survey"]
                                       .format(id=cursor.lastrowid, prefix=self.guild.config["prefix"]))

    async def post_survey(self, msg, command, args):
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return

        if len(args) != 1:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
            return
        try:
            survey_id = int(args[0])
        except ValueError:
            msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotANumberError"])
            return
        # Vérification de l'existance du sondage
        with self.guild.bot.database.cursor() as cursor:
            sql_id = "SELECT id FROM `{guild_id}surveys`".format(guild_id=self.guild.id)
            cursor.execute(sql_id)
            liste_id = [r["id"] for r in cursor.fetchall()]
        if survey_id not in liste_id:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["SurveyNotExistsError"])
            return
        # Verification que le sondage n'a pas déjà été publié
        with self.guild.bot.database.cursor() as cursor:
            sql_depart = "SELECT depart FROM `{guild_id}surveys` WHERE id = %s".format(guild_id=self.guild.id)
            cursor.execute(sql_depart, (survey_id))
            depart = cursor.fetchone()["depart"]
        if depart is not None:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["AlreadySendSurvey"])
            return
        # Envoi du sondage
        with self.guild.bot.database.cursor() as cursor:
            sql_update = "UPDATE `{guild_id}surveys` SET depart = %s WHERE id=%s" \
                .format(guild_id=self.guild.id)
            cursor.execute(sql_update, (int(time.time()), survey_id))
        self.guild.bot.database.commit()
        with self.guild.bot.database.cursor() as cursor:
            sql_choices = "SELECT id from `{guild_id}survey_choices` WHERE survey=%s" \
                .format(guild_id=self.guild.id)
            cursor.execute(sql_choices, (survey_id))
            choices_id = [r["id"] for r in cursor.fetchall()]
        with self.guild.bot.database.cursor() as cursor:
            sql_survey_title = "SELECT title, duree FROM `{guild_id}surveys` WHERE id = %s" \
                .format(guild_id=self.guild.id)
            cursor.execute(sql_survey_title, (survey_id))
            result = cursor.fetchone()
        # Envoi des messages de présentation
        await msg.channel.send(tr.tr[self.guild.config["lang"]]["modules"]["survey"]["post_survey"]["presentation"]
                               .format(prefix=self.guild.config["prefix"], heures=int(result["duree"] / 3600)))
        await msg.channel.send(result['title'])
        # Envoi des message pour chaque choix
        for choice_id in choices_id:
            with self.guild.bot.database.cursor() as cursor:
                sql_choice = "SELECT id,content, attachment, attachment_name FROM `{guild_id}survey_choices` WHERE id=%s" \
                    .format(guild_id=self.guild.id)
                cursor.execute(sql_choice, (choice_id))
                result = cursor.fetchone()
            if result["attachment_name"]:
                with open(result["attachment_name"], "wb") as temp_file:
                    temp_file.write(result["attachment"])
                with open(result["attachment_name"], "rb") as temp_file:
                    await msg.channel.send("`{prefix}vote {id}` "
                                           .format(prefix=self.guild.config["prefix"], id=result["id"]) + result[
                                               "content"],
                                           file=discord.File(temp_file, filename=str(result["attachment_name"])))
            else:
                await msg.channel.send(content="`{prefix}vote {id}` "
                                       .format(prefix=self.guild.config["prefix"], id=result["id"]) + result["content"])

    async def post_result(self, msg, command, args):
        # L'auteur est-t-il un admin?
        if msg.author.id not in self.guild.config["master_admins"]:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["PermissionError"])
            return
        # Nombre de paramètres
        if len(args) != 1:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotEnoughParamError"])
            return
        try:
            survey_id = int(args[0])
        except ValueError:
            msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotANumberError"])
            return
        # Vérification de l'existance du sondage
        with self.guild.bot.database.cursor() as cursor:
            sql_id = "SELECT id FROM `{guild_id}surveys`".format(guild_id=self.guild.id)
            cursor.execute(sql_id)
            liste_id = [r["id"] for r in cursor.fetchall()]
        if survey_id not in liste_id:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["SurveyNotExistsError"])
            return
        # Vérification que le sondage est terminé
        with self.guild.bot.database.cursor() as cursor:
            # Récupération de la date de fin du sondage
            select_survey_sql = "SELECT depart, duree FROM `{guild_id}surveys` WHERE id=%s;".format(
                guild_id=self.guild.id)
            cursor.execute(select_survey_sql, (survey_id))
            r = cursor.fetchone()
        if r["depart"] is not None:
            fin = r["depart"] + r["duree"]
        else:
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotYetPostedError"])
            return
        print(fin, time.time())
        if fin > time.time():
            await msg.channel.send(tr.tr[self.guild.config["lang"]]["errors"]["NotYetFinishedError"])
            return

        # Récupération des choix
        with self.guild.bot.database.cursor() as cursor:
            sql_select_choices = "SELECT id FROM `{guild_id}survey_choices` WHERE survey=%s;".format(
                guild_id=self.guild.id)
            cursor.execute(sql_select_choices, (survey_id))
            choices = [r["id"] for r in cursor.fetchall()]

        # Récupération des votes
        votes = []
        for id_choice in choices:
            with self.guild.bot.database.cursor() as cursor:
                select_votes_sql = "SELECT id FROM `{guild_id}survey_votes` WHERE choice=%s;".format(
                    guild_id=self.guild.id)
                cursor.execute(select_votes_sql, (id_choice))
                votes.append((id_choice, len(cursor.fetchall())))

        votes.sort(key=lambda x: x[1])
        total = sum([x[1] for x in votes])
        texte = tr.tr[self.guild.config["lang"]]["modules"]["survey"]["result"]["text"] + "```"
        i = 0
        for vote in votes[::-1]:
            i += 1
            texte += "\n n°{i} - Choix {id_choix} - {nb_votes} ({pourcentage}%)" \
                .format(i=i, id_choix=vote[0], nb_votes=vote[1], pourcentage=vote[1] * 100 / total)
        texte += "```"
        await msg.channel.send(texte)

    async def on_message(self, msg):
        if msg.content.startswith(self.guild.config["prefix"]):
            command, *args = msg.content.lstrip(self.guild.config["prefix"]).split(" ")
            if command == "vote":
                await self.vote(msg, command, args)
            elif command == "add_choice":
                await self.add_choice(msg, command, args)
            elif command == "create_survey":
                await self.create_survey(msg, command, args)
            elif command == "post_survey":
                await self.post_survey(msg, command, args)
            elif command == "post_results":
                await self.post_result(msg, command, args)
        return
