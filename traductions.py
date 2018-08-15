tr = {
    "FR_fr": {
        "modules": {
            "modules": {
                "description": "Permet de gérer les modules.",
                "aide": {
                    "list_modules": {
                        "description": "Liste tous les modules. Les modules en gras sont activés.",
                        "exemples": [
                            ("`list_modules`", "Liste tous les modules"),
                        ],
                    },
                    "load": {
                        "description": "Permet de charger un ou des modules.",
                        "exemples": [
                            ("`load fun`", "Charge le module fun"),
                            ("`load fun admin`", "Charge les modules fun et admin"),
                        ],
                    },
                    "unload": {
                        "description": "Permet de décharger un ou des modules.",
                        "exemples": [
                            ("`unload fun`", "Décharge le module fun"),
                            ("`unload fun admin`", "Décharge les modules fun et admin"),
                        ],
                    },
                },
                "list_modules": {
                    "title": "Liste des modules",
                },
                "load": {
                    "error": {
                        "name": "Erreur lors de l'activation du module %s:",
                        "value": "Celui-ci n'existe pas. Tapez %slist_modules pour voir la liste des modules disponibles.",
                        "title": "Erreur",
                    },
                    "permissionError": {
                        "title": "Erreur",
                        "one": {
                            "name": "Erreur lors du chargement du module.",
                            "value": "Vous n'avez pas la permission de charger un module.",
                        },
                        "many": {
                            "name": "Erreur lors du chargement des modules.",
                            "value": "Vous n'avez pas la permission de charger des modules."
                        }
                    },
                    "unload": {
                        "error": {
                            "name": "Erreur lors de la désactivation du module %s:",
                            "value": "Celui-ci n'existe pas ou n'est pas activé. Tapez %slist_modules pour voir la liste des modules disponibles.",
                            "title": "Erreur",
                        },
                        "permissionError": {
                            "title": "Erreur",
                            "one": {
                                "name": "Erreur lors de la désactivation du module.",
                                "value": "Vous n'avez pas la permission de désactiver  un module.",
                            },
                            "many": {
                                "name": "Erreur lors de la désactivation des modules.",
                                "value": "Vous n'avez pas la permission de désactiver des modules."
                            },
                        },
                    },
                },
            },
        },
    },
    "EN_us": {
        "modules": {
            "modules": {
                "description": "Allow to manage modules.",
                "aide": {
                    "list_modules": {
                        "description": "Lists all modules. Modules in bold are enabled.",
                        "exemples": [
                            ("`list_modules`", "Lists all modules"),
                        ],
                    },
                    "load": {
                        "description": "Load one or more modules.",
                        "examples": [
                            ("`load fun`", "Load fun module"),
                            ("`load fun admin`", "Load fun and admin modules"),
                        ],
                    },
                    "unload": {
                        "description": "Unload one or more modules.",
                        "exemples": [
                            ("`load fun`", "Unload fun module"),
                            ("`upload fun admin`", "Unload fun and admin modules"),
                        ],
                    },
                },
                "list_modules": {
                    "title": "List of modules"
                },
                "load": {
                    "error": {
                        "name": "Error when activating the %s module:",
                        "value": "This one doesn't exist. Type %slist_modules to see the list of available modules.",
                        "title": "Error",
                    },
                    "permissionError": {
                        "title": "Error",
                        "one": {
                            "name": "Error when loading the module.",
                            "value": "You do not have permission to load a module.",
                        },
                        "many": {
                            "name": "Error when loading modules.",
                            "value": "You do not have permission to load modules.",
                        },
                    },
                },
                "unload": {
                    "error": {
                        "name": "Error when deactivating the %s module:",
                        "value": "This one doesn't exist or isn't activate. Type %slist_modules to see the list of available modules.",
                        "title": "Error",
                    },
                    "permissionError": {
                        "title": "Error",
                        "one": {
                            "name": "Error when deactivating the module.",
                            "value": "You do not have permission to deactivate a module.",
                        },
                        "many": {
                            "name": "Error when deactivate modules.",
                            "value": "You do not have permission to deactivate modules.",
                        },
                    },
                },
            },
        },
    },
}
