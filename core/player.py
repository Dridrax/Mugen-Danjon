#class/player.py

class Player:
    def __init__(self):
        # -------------------------
        # STATS BASE
        # -------------------------
        self.hp_max = 100
        self.hp = self.hp_max

        self.ataque_base = 10
        self.defensa_base = 5

        # -------------------------
        # PROGRESO
        # -------------------------
        self.piso = 1
        self.habitacion = 0

        # -------------------------
        # ECONOMÍA
        # -------------------------
        self.oro = 0

        # -------------------------
        # INVENTARIO
        # -------------------------
        self.inventario = []

        # -------------------------
        # EQUIPAMIENTO (1 arma)
        # -------------------------
        self.arma_equipada = None

    # -------------------------
    # ESTADO
    # -------------------------

    def esta_vivo(self):
        return self.hp > 0

    # -------------------------
    # STATS EFECTIVOS
    # -------------------------

    def get_ataque(self):
        bonus = 0

        if self.arma_equipada and "stats" in self.arma_equipada.__dict__:
            bonus += self.arma_equipada.stats.get("ataque", 0)

        return self.ataque_base + bonus

    def get_defensa(self):
        return self.defensa_base

    # -------------------------
    # VIDA
    # -------------------------

    def recibir_dano(self, dano):
        dano_final = max(0, dano - self.get_defensa())
        self.hp -= dano_final
        return dano_final

    def curar(self, cantidad):
        self.hp = min(self.hp_max, self.hp + cantidad)

    # -------------------------
    # INVENTARIO
    # -------------------------

    def agregar_item(self, item):
        self.inventario.append(item)

    def agregar_oro(self, cantidad):
        self.oro += cantidad

    # -------------------------
    # EQUIPAMIENTO
    # -------------------------

    def equipar_arma(self, item):
        """
        Solo permite equipar armas.
        """
        if item.tipo != "arma":
            return False

        self.arma_equipada = item
        return True

    def cambiar_arma(self, item_nueva):
        """
        Devuelve el arma anterior si existía.
        """
        arma_anterior = self.arma_equipada
        self.arma_equipada = item_nueva
        return arma_anterior

    # -------------------------
    # UTILIDAD (para UI futura)
    # -------------------------

    def get_estado(self):
        return {
            "hp": self.hp,
            "hp_max": self.hp_max,
            "ataque": self.get_ataque(),
            "defensa": self.get_defensa(),
            "oro": self.oro,
            "arma": self.arma_equipada.nombre if self.arma_equipada else None
        }

    def get_inventario(self):
        return [item.nombre for item in self.inventario]