# Structure : ID_UNIQUE -> {Nom, Description, Remédiation}
PEDAGOGY_DB = {
    # --- COMPRÉHENSION DU NOMBRE ---
    "CONF_CHIFFRE_NOMBRE": {
        "category": "Compréhension du nombre",
        "name": "Confusion chiffre/nombre",
        "example": "Dans 145, l'élève dit que le nombre de dizaines est 4 (au lieu de 14).",
        "remediation": "Utilise l'analogie des paquets. 'Le chiffre, c'est l'étiquette sur la colonne. Le nombre, c'est combien de paquets de 10 on a en tout'."
    },
    "CONSTRUCT_NB": {
        "category": "Compréhension du nombre",
        "name": "Construction du nombre",
        "example": "L'écrit 6013 pour 'soixante-treize' ou 10020 pour 'cent-vingt'.",
        "remediation": "Utilise le tableau de numération (CDU). Demande à l'élève de placer les chiffres dans les colonnes."
    },
    
    # --- COMPTINE NUMÉRIQUE ---
    "PASSAGE_DIZAINE": {
        "category": "Comptine numérique",
        "name": "Passage de la dizaine",
        "example": "Après 29, l'élève ne sait plus ou dit 'dix-neuf' ou 'trente-dix'.",
        "remediation": "Reviens à la bande numérique ou au boulier. Fais visualiser le changement de famille."
    },

    # --- AUTOMATISMES ---
    "TABLE_MULT_INV": {
        "category": "Automatismes",
        "name": "Erreur Table de Multiplication",
        "example": "7 x 8 = 54",
        "remediation": "Ne donne pas la réponse. Demande une méthode de reconstruction (ex: 7x8 c'est 7x4 et encore 7x4, ou 7x10 moins 7x2)."
    },
    "COMPLEMENT_10": {
        "category": "Automatismes",
        "name": "Compléments à 10/100",
        "example": "Pour aller de 7 à 10, il dit 2.",
        "remediation": "Fais utiliser les doigts ou la maison du 10. Visualisation des amis de 10."
    },

    # --- STRATÉGIE / PROCÉDURE ---
    "OUBLI_RETENUE": {
        "category": "Stratégie/Procédure",
        "name": "Oubli de retenue",
        "example": "Dans une addition ou multiplication posée, la retenue n'est pas comptée.",
        "remediation": "Demande de refaire le calcul en verbalisant. 'As-tu pensé à ce qui dépasse de la boîte des unités ?'."
    },
    "MAUVAIS_ALIGNEMENT": {
        "category": "Stratégie/Procédure",
        "name": "Mauvais alignement UDC",
        "example": "Pose l'opération en alignant à gauche ou n'importe comment.",
        "remediation": "Fais tracer des colonnes verticales ou utilise du papier quadrillé. 'Les unités sous les unités'."
    },
    
    # Cas par défaut
    "UNKNOWN": {
        "category": "Autre",
        "name": "Erreur non classifiée",
        "example": "Cas général",
        "remediation": "Guide l'élève pas à pas sans donner la réponse."
    }
}

# Liste allégée pour le prompt du LLM (pour économiser des tokens)
# On ne lui donne que les clés et les noms pour qu'il choisisse.
ERROR_LIST_FOR_PROMPT = "\n".join([f"- {key}: {val['name']} ({val['category']})" for key, val in PEDAGOGY_DB.items()])