ENEMIES = {
    "goblin": {
        "nombre": "Goblin",
        "tipo": "normal",
        "stats": {
            "hp": 30,
            "ataque": 8,
            "defensa": 2
        },
        "drop": [
            {"item_id": "oro_10", "probabilidad": 0.7},
            {"item_id": "daga_oxidada", "probabilidad": 0.3}
        ],
        "peso": 25
    },

    "slime": {
        "nombre": "Slime",
        "tipo": "normal",
        "stats": {
            "hp": 10,
            "ataque": 4,
            "defensa": 1
        },
        "drop": [
            {"item_id": "oro_5", "probabilidad": 0.8},
            {"item_id": "daga_oxidada", "probabilidad": 0.1}
        ],
        "peso": 50
    },

    "popo": {
        "nombre": "Popo",
        "tipo": "normal",
        "stats": {
            "hp": 1,
            "ataque": 1,
            "defensa": 0
        },
        "drop": [
            {"item_id": "pocion_pequena", "probabilidad": 1},
            {"item_id": "oro_1", "probabilidad": 0.1}
        ],
        "peso": 35
    },

    "goblin_king": {
        "nombre": "Rey Goblin",
        "tipo": "boss",
        "stats": {
            "hp": 80,
            "ataque": 12,
            "defensa": 4
        },
        "peso": 1,
        "drop": [
            {"item_id": "oro_10", "probabilidad": 1},
            {"item_id": "soul_king_goblin0", "probabilidad": 0.1}
        ]

    }
}