tr = {
    "FR_fr": {
        "description": "Français",
        "modules": {
            "modules": {
                "description": "Permet de gérer les modules.",
                "help": {
                    "list_modules": {
                        "description": "Liste tous les modules. Les modules en gras sont activés.",
                        "examples": [
                            ("`{prefix}list_modules`", "Liste tous les modules"),
                        ],
                    },
                    "load": {
                        "description": "Permet de charger un ou des modules.",
                        "examples": [
                            ("`{prefix}load fun`", "Charge le module fun"),
                            ("`{prefix}load fun admin`", "Charge les modules fun et admin"),
                        ],
                    },
                    "unload": {
                        "description": "Permet de décharger un ou des modules.",
                        "examples": [
                            ("`{prefix}unload fun`", "Décharge le module fun"),
                            ("`{prefix}unload fun admin`", "Décharge les modules fun et admin"),
                        ],
                    },
                },
                "list_modules": {
                    "title": "Liste des modules",
                },
                "load": {
                },
                "unload": {
                },
            },
            "config": {
                "description": "Configuration de foBot, doublez le préfixe pour y accéder.",
                "help": {
                    "lang": {
                        "description": "Modifier la langue",
                        "examples": [
                            ("`{prefix}{prefix}lang FR_fr`", "Change la langue en français"),
                        ],
                    },
                    "list_lang": {
                        "description": "Liste les langues disponibles",
                        "examples": [
                            ("`{prefix}{prefix}list_lang`", "Affiche toutes les langues disponibles.")
                        ]
                    },
                    "set": {
                        "description": "Modifie un paramètre",
                        "examples": [
                            ("`{prefix}{prefix}set prefix %`", "Change le préfixe en `%`"),
                        ],
                    },
                    "list": {
                        "description": "Liste des paramètres disponibles",
                        "examples": [
                            ("`{prefix}{prefix}list`", "Liste des paramètres modifiables")
                        ],
                    },
                    "add_master_admin": {
                        "description": "Ajoute un administrateur du bot",
                        "examples": [
                            ("`{prefix}{prefix}add_master_admin <@unemention>`",
                             "Ajoute <@unemention> aux administrateurs du bot"),
                            ("`{prefix}{prefix}add_master_admin <@unemention>, <@unemention2>`",
                             "Ajoute <@unemention> et <@unemention1> aux administrateurs du bot"),
                        ],
                    },
                    "del_master_admin": {
                        "description": "Supprime un administrateur du bot",
                        "examples": [
                            ("`{prefix}{prefix}del_master_admin <@unemention>`",
                             "Supprime <@unemention> des administrateurs du bot"),
                            ("`{prefix}{prefix}add_master_admin <@unemention>, <@unemention2>`",
                             "Supprime <@unemention> et <@unemention1> des administrateurs du bot"),
                        ],
                    },
                },
                "lang": "La langue {lang} est maintenant utilisée.",
                "list_lang": {
                    "title": "Langues disponibles",
                },
                "list": {
                    "title": "Liste des paramètres modifiables",
                    "params": {
                        "prefix": "Préfixe utilisé par le bot."
                    }
                },
                "add_master_admin": "L'utilisateur {user} est maintenant un administrateur du bot.",
                "del_master_admin": "L'utilisateur {user} n'est plus un administrateur du bot.",
            },
            "help": {
                "description": "Active la commande d'aide",
                "help": {
                    "help": {
                        "description": "Permat d'aficher de l'aide",
                        "examples": [
                            ("`{prefix}help`", "Affiche l'aide générale"),
                            ("`{prefix}help config`", "Liste les commandes disponibles dans le module config"),
                            ("`{prefix}help config:lang`", "Affiche l'aide avancé de la commande lang u module config"),
                        ],
                    },
                },
            },
            "pi": {
                "description": "Commandes relatives au nombre pi",
                "help": {
                    "pi": {
                        "description": "Donne 2000 décimales de pi.",
                        "examples": [
                            ("`(prefix}pi`", "Affiche les 2000 premières décimales de pi."),
                            ("`{prefix}pi 2000`", "Affiche 2000 décimales de pi à partir de la 2000ème"),
                        ],
                    }, "fpi": {
                        "description": "Recherche l'expression régulière dans pi",
                        "examples": [
                            ("`{prefix}fpi 12345`", "Affiche les 10 premières occurences de 12345 dans pi"),
                            ("`{prefix}fpi 20?2?1`", "Affiche les 10 premières occurences de 21, 201, 221 et 2021")
                        ],
                    },
                },
                "pi": "Voici les 2000 décimales de pi que vous avez demandé (à partir de la {debut}ème):",
                "fpi": "Une occurence de votre recherche a été trouvée à la {debut}ème place: `{before}`{find}`{after}`",
            },
            "avalon": {
                "description": "Commandes relatives au jeu avalon",
                "help": {
                    "avalonstats": {
                        "description": "Donne les stats du jeu avalon sur le serveur",
                        "examples": [
                            ("`{prefix}`avalonstats", "Affiche les stats des parties avalon du serveur"),
                        ],
                    },
                    "avalonjoin": {
                        "description": "Rejoindre la liste d'attente des joueurs pour avalon",
                        "examples": [
                            ("`{prefix}avalonjoin`", "Rejoindre la liste d'attente d'une partie avalon"),
                        ],
                    },
                    "avalonstart": {
                        "description": "Lancer la partie d'avalon",
                        "examples": [
                            ("`{prefix}`avalonstart", "Lance la partie d'avalon si il ya a assez de joueurs.")
                        ]
                    }
                },
                "avalonstats": "Depuis la création du jeu sur ce serveur {nb_games} parties de avalon ont étés jouées, "
                               "les gentils ont gagnés {nb_victoire_gentil} et les méchants ont gagnés "
                               "{nb_victoire_mechant}",
                "avalonjoin": {
                    "join": "<@{player_id}>, vous avec rejoint la partie avalon, il y a actuellement {nb_players} "
                            "joueurs dans cette partie",
                    "canplay": "Il y a maintenant assez de joueurs, tapez `{prefix}avalonstart` pour démarer la partie.",
                    "alreadyplay": "Vous ne pouvez pas jouer à deux parties en même temps.",
                    "alreadywaiting": "Vous attendez déja de pouvoir jouer",
                },
                "avalonquit": {
                    "quit": "<@{player_id>, vous avez bien quitté la partie, il reste {nb_players} joueurs",
                    "alreadyplaying": "<@{player_id}> vous êtes dans une partie déjà commencé, tous les joueurs de la "
                                      "partie doivent quitter pour que la partie se termine."
                },
                "avalonstart": {
                    "start": "La partie est lancée, avec {nb_joueurs}. Les roles {liste_roles} sont présents. Bonne "
                             "partie!",
                    "roles": {
                        "gentil": "gentil",
                        "mechant": "mechant",
                        "merlin": "merlin",
                        "assassin": "assassin",
                        "mordred": "mordred",
                        "perceval": "perceval",
                        "morgane": "morgane",
                        "oberon": "obéron"
                    },
                    "bienvenue": "Je vous souhaite à tous la bienvenue autour de cette table ronde, maleuresement au moins "
                             "deux méchants sont présents. Leur but est de faire échouer trois quêtes du roi arthur, ou "
                             "de refuser cinq écuipes de quêtes d'affilé. Le roi arthur va proposer cinq quêtes, vous "
                             "devrez pour chacunes composer un équipe, la faire valider par les autres et réussir la "
                             "quête."
                },
            },
            "github": {
                "description": "Commands relatives à discord",
                "help": {
                    "sourcecode": {
                        "description": "Donne un lien vers mon code source (il est là comme ca tu a pas retapper la \
commande :smile: https://github.com/Fomys/foBot",
                        "examples": [
                            ("`{prefix}`sourcecode", "Affiche mon code source")
                        ]
                    },
                },
                "sourcecode": "Mon code source est disponible sur github: https://github.com/Fomys/foBot",
            },
            "tools": {
                "description": "Commandes utiles",
                "help": {
                    "ping": {
                        "description": "Renvoie le temps de réponse du bot",
                        "examples": [
                            ("`{prefix}ping`", "Affiche le temps de réponse du bot"),
                        ],
                    },
                },
                "ping": {
                    "title": "Pong!"

                }
            },
        },
        "errors": {
            "LangNotFoundError": "La langue {lang} est introuvable, tapez {prefix}list_lang pour voir les langues "
                                 "disponibles.",
            "PermissionError": "Vous n'avez pas la permission de faire cette action.",
            "ModuleNotFoundOrDeactivatedError": {
                "title": "Erreur",
                "name": "Erreur lors de la désactivation du module {module}:",
                "value": "Celui-ci n'existe pas ou n'es pas activé. Tapez {prefix}list_modules pour voir la liste des "
                         "modules disponibles.",

            },
            "ModuleNotFoundError": {
                "title": "Erreur",
                "name": "Erreur lors de l'activation du module {module}:",
                "value": "Celui-ci n'existe pas. Tapez {prefix}list_modules pour voir la liste des modules "
                         "disponibles.",
                "text": "Le module {module} n'existe pas, tapez {prefix}list_modules pour voir la liste des modules "
                        "disponibles.",
            },
            "ForbiddenConfigError": "Ce paramètre ne peut pas être modifié directement.",
            "UnknownConfigError": "Le paramètre demandé n'existe pas. Utilisez {prefix}list pour lister les paramètres "
                                  "modifiables.",
            "NotEnoughParamError": "Il manque un ou plusieurs parametres à la commande.",
            "NoMentionsError": "Vous devez mentioner un utilisateur pour le rajouter à la liste des administrateurs "
                               "du bot.",
            "CommandNotFoundError": "La commande {command} n'existe pas.",
            "TooBigNumberPiError": "Vous devez spécifier un nombre inferieur a 1000000.",
            "RegexError": "La regex que vous avez utilisé n'est pas valide.",
            "ForbiddenRegexError": "Vous n'avez pas le droit d'utiliser les caractères `*` et `+` dans une regex.",
            "RegexTooLongError": "La regex ne doit pas faire plus e 50 caractères",
            "PiFileError": "Les décimales de pi sont indisponibles, veuillez réessayer plus tard...",
        },
    },
}
