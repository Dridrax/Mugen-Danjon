from core.player import Player
from core.dungeon.dungeon_run import DungeonRun



def main():

    # =========================
    # CREAR PLAYER
    # =========================
    nombre_player = input("¿Cual es tu nombre aventurero?: ")
    jugador = Player(nombre_player)

    # =========================
    # CREAR COMBATE
    # =========================
    run = DungeonRun(jugador)

    # =========================
    # INICIAR COMBATE
    # =========================
    run.start()

if __name__ == "__main__":
    main()