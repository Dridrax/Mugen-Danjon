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

        self.stat_points = 0
        self.skill_points = 0

        self.exp_siguiente_nivel = self.calcular_exp_siguiente()

        self.habilidades = [
            "ataque_basico",
            "cura_base"
        ]

        self.skill_levels = {
            "ataque_basico": 1,
            "cura_base": 1
        }

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
    
    def subir_stat(self, stat):

        if self.stat_points <= 0:
            print("\nNo tienes puntos de stats.")
            return
        
        if stat == "hp":
    
            self.hp_max += 5
            self.hp += 5

            print("\nHP máximo aumentado +5")

        elif stat == "ataque":

            self.ataque_base += 2

            print("\nAtaque aumentado +2")

        elif stat == "defensa":

            self.defensa_base += 1

            print("\nDefensa aumentada +1")

        else:
            print("\nStat inválido.")
            return
        
        self.stat_points -= 1

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
        puntos_ganados = 5
        self.stat_points += puntos_ganados

        if self.nivel % 2 == 0:
            self.skill_points += 1

            print("-Obtuviste 1 Skill Point.")

        # Curación completa al subir nivel
        self.hp = self.hp_max

        # Nueva experiencia requerida
        self.exp_siguiente_nivel = self.calcular_exp_siguiente()


        print(f"\n-{self.nombre} SUBE A NIVEL {self.nivel}!")
        print(f"-Obtienes {puntos_ganados} puntos de stat.")

    def distribuir_stats(self):

        while self.stat_points > 0:

            print(f"\nPuntos disponibles: {self.stat_points}")

            self.mostrar_stats()

            print("\nMejorar:")
            print("1. HP (+5)")
            print("2. ATK (+2)")
            print("3. DEF (+1)")
            print("4. Salir.")

            opcion = input("Elige stat: ")

            if opcion == "1":
                self.subir_stat("hp")

            elif opcion == "2":
                self.subir_stat("ataque")

            elif opcion == "3":
                self.subir_stat("defensa")

            elif opcion == "4":
                break

    def aprender_skill(self, skill_id):

        if skill_id in self.habilidades:
            print("\nYa conoces esta habilidad.")
            return
        self.habilidades.append(skill_id)

        self.skill_levels[skill_id] = 1

        print(
            f"\Aprendes "
            f"{SKILLS[skill_id]['nombre']}")
        
    def get_skill_power(self, skill_id):
        nivel = self.skill_levels[skill_id]
        
        return SKILLS[skill_id]["scaling"][nivel]
    

    def mejorar_skill(self, skill_id):

        if self.skill_points <= 0:

            print("\nNo tienes Skill Points.")
            return

        nivel_actual = self.skill_levels[skill_id]

        max_level = SKILLS[skill_id]["max_level"]

        if nivel_actual >= max_level:

            print("\nLa habilidad ya está al máximo.")
            return

        self.skill_levels[skill_id] += 1

        self.skill_points -= 1

        print(
            f"\n{SKILLS[skill_id]['nombre']} "
            f"sube a nivel "
            f"{self.skill_levels[skill_id]}"
        )
        
    # =========================
    # ACCIONES (EJECUCIÓN)
    # =========================
    def ejecutar_habilidad(self, skill_id, objetivo):

        skill = SKILLS[skill_id]

        if skill["tipo"] == "daño":

            power = self.get_skill_power(skill_id)

            dano = self.get_ataque() * power

            recibido = objetivo.recibir_dano(dano)

            print(
                f"-> Usas {skill['nombre']} "
                f"contra {objetivo.nombre} "
                f"e infliges {recibido} de daño."
            )

        elif skill["tipo"] == "curacion":

            cantidad = self.get_skill_power(skill_id)

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
    
    def mostrar_stats(self):

        print(f"\n{self.nombre}")
        print(f"HP: {self.hp}/{self.hp_max}")
        print(f"ATK: {self.ataque_base}")
        print(f"DEF: {self.defensa_base}")
        print(f"Stat Points: {self.stat_points}")
        print(f"Skill Point: {self.skill_points}")

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