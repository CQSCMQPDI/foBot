tr = {
    "FR_fr": {
        "description": "Français",
        "modules": {
            "modules": {
                "description": "Gestion des modules.",
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
            "deeptown": {
                "description": "Commandes relatives au jeu deeptown.",
                "help": {
                    "best_place_mine": {
                        "description": "Montre les meilleurs emplacements de mine pour un cerain minerais.",
                        "examples": [
                            ("`{prefix}best_place_mine iron`",
                             "Donne les meilleurs emplaceent pour le minerais de fer.")
                        ],
                    },
                    "to_make": {
                        "description": "Donne les resource nécessaires pour faire un item.",
                        "example": [
                            ("`{prefix}to_make copperNail 100`",
                             "Donne les resources pour faire 100 clous en cuivre, càd 10 copperBar."),
                        ],
                    },
                    "to_make_recursive": {
                        "description": "Donne toutes les resources nécessaires pour faire un item.",
                        "example": [
                            ("`{prefix}to_make_recursive copperNail 100`",
                             "Donne les resources pour faire 100 copperNail, càd 10 copperBar et 50 copper."),
                        ],

                    }
                },
                "best_place_mine": "Voici les meilleurs emplacements pour le minerais {ore}\n```\n",
                "to_make": "Pour faire {quantity} {item} il faudra {time}. Il vous faudra {needed}. La valeur totale "
                           "de la production est {value}.",
                "recursive_to_make": {
                    "header": "Pour faire {quantity} {item} il vous faudra:\n```",
                    "line": "{item:20} | {quantity} | {time}"
                },
            },
            "help": {
                "description": "Active la commande d'aide",
                "help": {
                    "help": {
                        "description": "Permat d'aficher de l'aide",
                        "examples": [
                            ("`{prefix}help`", "Affiche l'aide générale"),
                            ("`{prefix}help config`", "Liste les commandes disponibles dans le module config"),
                            ("`{prefix}help config:lang`",
                             "Affiche l'aide avancé de la commande lang u module config"),
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
                    },"fpi": {
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
            "github": {
                "description": "Commands relatives à discord",
                "help": {
                    "sourcecode": {
                        "description": "Donne un lien vers mon code source (il est là comme ca tu a pas retapper la \
commande :smile: https://github.com/Fomys/foBot",
                        "examples":[
                            ("`prefix`sourcecode", "Affiche mon code source")
                        ]
                    },
                },
                "sourcecode":"Mon code source est disponible sur github: https://github.com/Fomys/foBot",
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
            "OreNotFoundError": "{ore} n'est pas un minerais valide.",
            "NotIntError": "{number} n'est pas un nombre entier valide.",
            "ItemNotFoundError": "{item} n'extiste pas dans deeptown",
            "CommandNotFoundError": "La commande {command} n'existe pas.",
            "TooBigNumberPiError": "Vous devez spécifier un nombre inferieur a 1000000.",
            "RegexError": "La regex que vous avez utilisé n'est pas valide.",
            "ForbiddenRegexError": "Vous n'avez pas le droit d'utiliser les caractères `*` et `+` dans une regex.",
            "RegexTooLongError": "La regex ne doit pas faire plus e 50 caractères",
            "PiFileError": "Les décimales de pi sont indisponibles, veuillez réessayer plus tard...",
        },
    },
}
