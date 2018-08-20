tr = {
    "FR_fr": {
        "description": "Français",
        "modules": {
            "modules": {
                "description": "Gestion des modules.",
                "aide": {
                    "list_modules": {
                        "description": "Liste tous les modules. Les modules en gras sont activés.",
                        "exemples": [
                            ("`{prefix}list_modules`", "Liste tous les modules"),
                        ],
                    },
                    "load": {
                        "description": "Permet de charger un ou des modules.",
                        "exemples": [
                            ("`{prefix}load fun`", "Charge le module fun"),
                            ("`{prefix}load fun admin`", "Charge les modules fun et admin"),
                        ],
                    },
                    "unload": {
                        "description": "Permet de décharger un ou des modules.",
                        "exemples": [
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
                "aide": {
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
                        "title": "Liste des Paramètres disponibles",
                        "params": {
                            "prefix": "Le préfixe utilisé sur le serveur",
                        },
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
                "aide":{

                },
                "best_place_mine":"Voici les meilleurs emplacements pour le minerais {ore}\n```\n",
                "to_make":"Pour faire {quantity} {item} il faudra {time}. Il vous faudra {needed}. La valeur totale de la production est {value}.",
                "recursive_to_make":{
                    "header":"Pour faire {quantity} {item} il vous faudra:\n```",
                    "line":"{item:20} | {quantity} | {time}"
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
                "value": "Celui-ci n'existe pas ou n'es pas activé. Tapez {prefix}list_modules pour voir la liste des modules disponibles.",

            },
            "ModuleNotFoundError": {
                "title": "Erreur",
                "name": "Erreur lors de l'activation du module {module}:",
                "value": "Celui-ci n'existe pas. Tapez {prefix}list_modules pour voir la liste des modules "
                         "disponibles.",
            },
            "ForbiddenConfigError": "Ce paramètre ne peut pas être modifié directement.",
            "UnknownConfigError": "Le paramètre demandé n'existe pas. Utilisez {prefix}list pour lister les paramètres "
                                  "modifiables.",
            "NotEnoughParamError": "Il manque un ou plusieurs parametres à la commande.",
            "NoMentionsError": "Vous devez mentioner un utilisateur pour le rajouter à la liste des administrateurs "
                               "du bot.",
            "OreNotFoundError": "{ore} n'est pas un minerais valide.",
            "NotIntError":"{number} n'est pas un nombre entier valide.",
            "ItemNotFoundError":"{item} n'extiste pas dans deeptown",
        },
    },
}
