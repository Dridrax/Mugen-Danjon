"""Tipos de comportamiento:

Normal: Se comporta normal

Lengo: Toma decisiones mas tranquilo

Tonto: Toma decisiones estupidas

Astuto: Toma decisiones mas acertadas"""

ENEMIES = {
    "goblin": {
        "nombre": "Goblin",
        "tipo": "normal",
        "nivel": 1,
        "comportamiento": "normal",
        "stats": {
            "hp": 30,
            "ataque": 12,
            "defensa": 2,
            "inteligencia": 0.3
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
        "nivel": 1,
        "comportamiento": "normal",
        "stats": {
            "hp": 10,
            "ataque": 10,
            "defensa": 1,
            "inteligencia": 0.2
        },
        "drop": [
            {"item_id": "oro_5", "probabilidad": 0.8},
            {"item_id": "daga_oxidada", "probabilidad": 0.1}
        ],
        "peso": 50
    },

    "mono_joven": {
        "nombre": "Mono Joven",
        "tipo": "normal",
        "nivel": 1,
        "comportamiento": "agresivo",
        "stats": {
            "hp": 15,
            "ataque": 11,
            "defensa": 2,
            "inteligencia": 0.6
        },
        "drop": [
            {"item_id": "oro_5", "probabilidad": 0.7}
        ],
        "peso": 55
    },

    "popo": {
        "nombre": "Popo",
        "tipo": "normal",
        "nivel": 1,
        "comportamiento": "miedoso",
        "stats": {
            "hp": 1,
            "ataque": 1,
            "defensa": 9,
            "inteligencia": 0.1
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
        "nivel": 5,
        "comportamiento": "agresivo",
        "stats": {
            "hp": 80,
            "ataque": 15,
            "defensa": 4,
            "inteligencia": 0.5
        },
        "peso": 1,
        "drop": [
            {"item_id": "oro_10", "probabilidad": 1},
            {"item_id": "soul_king_goblin", "probabilidad": 0.1}
        ]
    }
}