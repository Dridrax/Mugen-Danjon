import random
from core.ia import ia_utilitaria as ia


class Enemigo:
    def __init__(self, enemy_id, data, piso=1):

        stats = data.get("stats", {})

        self.id = enemy_id
        self.nombre = data["nombre"]
        self.tipo = data.get("tipo", "normal")

        self.nivel_base = data.get("nivel", 1)
        self.nivel = self.nivel_base + (piso - 1)

        base_int = stats.get("inteligencia", 0.5)

        # Inteligencia
        if self.tipo == "boss":
            self.inteligencia = min(0.85, base_int + 0.15)
        else:
            self.inteligencia = base_int

        # Stats base
        self.hp = self.escalar_stat(stats.get("hp", 10))
        self.hp_actual = self.hp

        self.ataque = self.escalar_stat(stats.get("ataque", 1))
        self.defensa = self.escalar_stat(stats.get("defensa", 1))

        self.comportamiento = data.get("comportamiento", "normal")

        self.drop_table = data.get("drop", [])
        self.peso = data.get("peso", 1)

        # Curvas de personalidad
        self.MAPA_CURVAS = {
            "normal": ia.curva_lineal,
            "miedoso": ia.curva_panico,
            "agresivo": ia.curva_agresiva
        }

        # Sistema de acciones
        self.ACCIONES = {
            "atacar": self._accion_atacar,
            "defender": self._accion_defender,
            "curar": self._accion_curar
        }

    # =========================
    # ESCALADO
    # =========================
    def escalar_stat(self, valor):
        """
        Escala suavemente los stats según nivel
        """
        return int(valor * (1 + 0.12 * (self.nivel - 1)))

    # =========================
    # IA (DECISIÓN)
    # =========================
    def decidir_accion(self, contexto):

        # 1. Utilidades base
        u_atacar = ia.score_atacar(contexto, self)
        u_curar = ia.score_curar(contexto, self)
        u_defender = ia.score_defenderse(contexto, self)

        # 2. Curva de personalidad
        funcion_curva = self.MAPA_CURVAS.get(
            self.comportamiento,
            ia.curva_lineal
        )

        puntuaciones = {
            "atacar": funcion_curva(u_atacar),
            "curar": funcion_curva(u_curar),
            "defender": funcion_curva(u_defender)
        }

        # 3. Ruido según inteligencia
        caos = (1.0 - self.inteligencia) * 0.3

        for accion in puntuaciones:
            puntuaciones[accion] += random.uniform(-caos, caos)

        # 4. Elegir mejor acción
        mejor_accion = max(puntuaciones, key=puntuaciones.get)

        return mejor_accion

    # =========================
    # EJECUCIÓN (ACCIONES)
    # =========================
    def ejecutar_accion(self, jugador, accion):

        funcion = self.ACCIONES.get(accion)

        if funcion:
            funcion(jugador)

        else:
            print(f"-> {self.nombre} duda y no hace nada...")

    # =========================
    # IMPLEMENTACIÓN ACCIONES
    # =========================
    def _accion_atacar(self, jugador):

        dano = self.ataque
        recibido = jugador.recibir_dano(dano)

        print(f"-> El {self.nombre} ATACA e inflige {recibido} de daño.")

    def _accion_defender(self, jugador):

        # Aquí luego puedes meter buffs reales
        print(f"-> El {self.nombre} se pone en DEFENSA.")

    def _accion_curar(self, jugador):

        cura = 10

        self.hp_actual = min(
            self.hp,
            self.hp_actual + cura
        )

        print(f"-> El {self.nombre} se CURA {cura} HP.")

    # =========================
    # DAÑO
    # =========================
    def recibir_dano(self, cantidad):

        dano_final = max(0, cantidad - self.defensa)

        self.hp_actual -= dano_final
        self.hp_actual = max(0, self.hp_actual)

        return dano_final

    # =========================
    # XP SYSTEM
    # =========================
    def calcular_xp(self):

        poder_base = (
            self.hp * 0.6 +
            self.ataque * 1.5 +
            self.defensa * 1.2 +
            self.inteligencia * 10
        )

        multiplicador_nivel = 1 + (self.nivel * 0.18)

        # Boss = XP fija escalada
        if self.tipo == "boss":

            xp = poder_base * multiplicador_nivel * 3

            return int(xp)

        # Normales = XP variable
        xp_min = poder_base * multiplicador_nivel * 0.8
        xp_max = poder_base * multiplicador_nivel * 1.2

        variacion = random.uniform(0.75, 1.25)

        xp = random.uniform(xp_min, xp_max) * variacion

        return max(1, int(xp))