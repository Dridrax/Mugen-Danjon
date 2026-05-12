from core.data.skills import SKILLS
from core.enemy import Enemigo

class Player:
    def __init__(self, nombre):

        self.nombre = nombre

        self.hp_max = 20
        self.hp = self.hp_max

        self.ataque_base = 10
        self.defensa_base = 5

        self.nivel = 1
        self.exp = 0

        self.exp_siguiente_nivel = self.calcular_exp_siguiente()

        self.habilidades = [
            "ataque_basico",
            "cura_base"
        ]

        self.inventario = []
        self.oro = 0

    # =========================
    # ESTADO
    # =========================
    def esta_vivo(self):
        return self.hp > 0

    # =========================
    # STATS
    # =========================
    def get_ataque(self):
        return self.ataque_base

    def get_defensa(self):
        return self.defensa_base

    # =========================
    # VIDA
    # =========================
    def recibir_dano(self, cantidad):

        dano_final = max(0, cantidad - self.defensa_base)

        self.hp -= dano_final
        self.hp = max(0, self.hp)

        return dano_final

    def curar(self, cantidad):

        self.hp = min(
            self.hp_max,
            self.hp + cantidad
        )

    # =========================
    # EXPERIENCIA / NIVELES
    # =========================
    def calcular_exp_siguiente(self):
        """
        Curva de experiencia necesaria
        """

        return int(40 + (self.nivel ** 2.0) * 15)

    def ganar_xp(self, cantidad):

        print(f"\n-{self.nombre} gana {cantidad} EXP.")

        self.exp += cantidad

        while self.exp >= self.exp_siguiente_nivel:

            self.exp -= self.exp_siguiente_nivel

            self.subir_nivel()

    def subir_nivel(self):

        self.nivel += 1

        # =========================
        # ESCALADO DE STATS
        # =========================
        hp_ganado = 15
        atk_ganado = 3
        def_ganada = 2

        self.hp_max += hp_ganado
        self.ataque_base += atk_ganado
        self.defensa_base += def_ganada

        # Curación completa al subir nivel
        self.hp = self.hp_max

        # Nueva experiencia requerida
        self.exp_siguiente_nivel = self.calcular_exp_siguiente()

        # Nuevas habilidades
        self.ganar_skill()

        print(f"\n-{self.nombre} SUBE A NIVEL {self.nivel}!")
        print(f"-HP +{hp_ganado}")
        print(f"-ATK +{atk_ganado}")
        print(f"-DEF +{def_ganada}")

    def ganar_skill(self):

        if (
            self.nivel == 5 and
            "tajo_rapido" not in self.habilidades
        ):
            self.habilidades.append("tajo_rapido")

        if (
            self.nivel == 10 and
            "golpe_fuerte" not in self.habilidades
        ):
            self.habilidades.append("golpe_fuerte")

    # =========================
    # ACCIONES (EJECUCIÓN)
    # =========================
    def ejecutar_habilidad(self, skill_id, objetivo):

        skill = SKILLS[skill_id]

        if skill["tipo"] == "daño":

            dano = self.get_ataque() * skill["valor"]

            recibido = objetivo.recibir_dano(dano)

            print(
                f"-> Usas {skill['nombre']} "
                f"contra {objetivo.nombre} "
                f"e infliges {recibido} de daño."
            )

        elif skill["tipo"] == "curacion":

            cantidad = skill["valor"]

            self.curar(cantidad)

            print(
                f"-> Usas {skill['nombre']} "
                f"y te curas {cantidad} HP."
            )

    # =========================
    # INPUT (DECISIÓN HUMANA)
    # =========================
    def elegir_accion(self, enemigos_vivos):

        print("\nTus habilidades:")

        for i, s_id in enumerate(self.habilidades):

            print(f"{i+1}. {SKILLS[s_id]['nombre']}")

        s_idx = int(input("Elige habilidad: ")) - 1

        skill_id = self.habilidades[s_idx]

        skill = SKILLS[skill_id]

        objetivo = None

        if skill["tipo"] == "daño":

            t_idx = int(
                input(
                    f"¿A quién atacas? "
                    f"(1-{len(enemigos_vivos)}): "
                )
            ) - 1

            objetivo = enemigos_vivos[t_idx]

        return skill_id, objetivo

    # =========================
    # CONTEXTO IA
    # =========================
    def get_contexto(self):

        return {
            "hp": self.hp,
            "hp_max": self.hp_max,
            "nombre_player": self.nombre,
            "nivel": self.nivel,
            "esta_herido": self.hp < (self.hp_max * 0.3)
        }