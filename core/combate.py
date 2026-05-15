
from core.enemy import Enemigo
from core.player import Player


class Combate:
    def __init__(self, 
                 jugador: Player, 
                 enemigos: list[Enemigo],
                 floor_number=1,
                 room_number=1,
                 total_rooms=1):

        self.jugador = jugador
        self.enemigos = enemigos
        
        self.floor_number = floor_number
        self.room_number = room_number
        self.total_rooms = total_rooms
        
        self.turno = 1

    def enemigos_vivos(self):
        return [
            enemigo
            for enemigo in self.enemigos
            if enemigo.hp_actual > 0
        ]
    
    def combate_activo(self):
        return (
            self.jugador.esta_vivo()
            and
            len(self.enemigos_vivos()) > 0
        )
    
    def iniciar(self):
        print(
                f"\n{'='*20} "
                f"¡COMIENZA EL COMBATE! "
                f"{'='*20}"
            )
        
        while self.combate_activo():
            
            self.mostrar_estado()

            self.turno_jugador()

            self.procesar_muertes()

            if not self.combate_activo():
                break

            self.turno_enemigos()

            self.procesar_muertes()

            self.turno += 1

        self.finalizar_combate()

    def mostrar_estado(self):

        print(
            f"\n========== "
            f"PISO {self.floor_number} "
            f"| "
            f"SALA {self.room_number}/{self.total_rooms} "
            f"=========="
        )
        
        print(f"\n========== TURNO {self.turno} ==========")

        print(
            f"\n{self.jugador.nombre} "
            f"| Lv.{self.jugador.nivel}"
        )

        print(
            f"HP: "
            f"{self.jugador.hp}/{self.jugador.hp_max}"
        )

        print(
            f"EXP: "
            f"{self.jugador.exp}/"
            f"{self.jugador.exp_siguiente_nivel}"
        )

        print(
            f"ATAQUE: "
            f"{self.jugador.ataque_base}"
        )

        print(
            f"DEFENSA: "
            f"{self.jugador.defensa_base}"
        )

        print(
            f"STAT POINTS: "
            f"{self.jugador.stat_points}"
        )

        print("\nEnemigos:")

        for i, enemigo in enumerate(self.enemigos_vivos()):
        
            print(
                f"[{i+1}] "
                f"{enemigo.nombre} "
                f"(Lv.{enemigo.nivel}) "
                f"HP: {enemigo.hp_actual}/{enemigo.hp}"
            )

    def turno_jugador(self):
        enemigos_vivos = self.enemigos_vivos()

        skill_id, objetivo = self.jugador.elegir_accion(
            enemigos_vivos
        )

        self.jugador.ejecutar_habilidad(
            skill_id= skill_id,
            objetivo= objetivo
        )

    def turno_enemigos(self):
        if not self.enemigos_vivos():
            return
        
        for enemigo in self.enemigos_vivos():
            if not self.jugador.esta_vivo():
                break

            contexto = self.jugador.get_contexto()

            accion = enemigo.decidir_accion(contexto)

            enemigo.ejecutar_accion(
                self.jugador,
                accion
            )

    def finalizar_combate(self):
        if self.jugador.esta_vivo():
            print("\n¡¡VICTORIA!!")

        else:
            print("\nHas sido derrotado...")

    def procesar_muertes(self):
        enemigos_derrotados = []

        for enemigo in self.enemigos:
            if enemigo.hp_actual <= 0:
                enemigos_derrotados.append(enemigo)

        for enemigo in enemigos_derrotados:

            print(
                f"\n{enemigo.nombre} "
                f"ha sido derrotado."
            )

            xp = enemigo.calcular_xp()

            self.jugador.ganar_xp(xp)

            self.enemigos.remove(enemigo)
