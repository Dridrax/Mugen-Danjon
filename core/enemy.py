import random
from core.item import Item


class Enemy:
    def __init__(self, enemy_id, data, piso=1):
        self.id = enemy_id
        self.nombre = data["nombre"]

        # Stats base escaladas por piso
        self.hp = data["stats"]["hp"] + (piso * 2)
        self.ataque = data["stats"]["ataque"] + (piso // 2)
        self.defensa = data["stats"]["defensa"] + (piso // 3)

        self.drop_table = data["drop"]
        self.peso = data.get("peso", 1)

        self.hp_actual = self.hp

    # -------------------------
    # ESTADO
    # -------------------------

    def esta_vivo(self):
        return self.hp_actual > 0

    def recibir_dano(self, dano):
        dano_final = max(0, dano - self.defensa)
        self.hp_actual -= dano_final
        return dano_final

    # -------------------------
    # DROP SYSTEM
    # -------------------------

    def generar_drop(self):
        drops = []

        for entry in self.drop_table:
            probabilidad = entry["probabilidad"]

            if random.random() < probabilidad:
                item_id = entry["item_id"]
                drops.append(Item(item_id))

        return drops

    # -------------------------
    # INFO (para UI futura)
    # -------------------------

    def get_estado(self):
        return {
            "nombre": self.nombre,
            "hp": self.hp_actual,
            "hp_max": self.hp,
            "ataque": self.ataque,
            "defensa": self.defensa
        }