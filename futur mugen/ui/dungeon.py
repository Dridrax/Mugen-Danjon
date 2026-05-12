import random


# -------------------------
# TIPOS DE SALA
# -------------------------

ROOM_COMBAT = "combat"
ROOM_REST = "rest"
ROOM_BOSS = "boss"


# -------------------------
# GENERAR PISO (SIMPLE)
# -------------------------

def generar_piso(piso):
    """
    Devuelve lista de salas para el piso
    versión simple: siempre 3 salas
    """

    return [
        {"type": ROOM_COMBAT, "visited": False},
        {"type": ROOM_REST, "visited": False},
        {"type": ROOM_BOSS, "visited": False}
    ]


# -------------------------
# ESTADO DE MAZMORRA
# -------------------------

class Dungeon:
    def __init__(self):
        self.piso = 1
        self.salas = generar_piso(self.piso)
        self.index_actual = 0

    def sala_actual(self):
        return self.salas[self.index_actual]

    def avanzar(self):
        self.salas[self.index_actual]["visited"] = True
        self.index_actual += 1

        # si termina el piso
        if self.index_actual >= len(self.salas):
            self.piso += 1
            self.salas = generar_piso(self.piso)
            self.index_actual = 0

    def get_estado(self):
        return {
            "piso": self.piso,
            "index": self.index_actual,
            "salas": self.salas
        }