from core.dungeon.rooms.room import Room
from core.dungeon.rooms.room_types import RoomType
from core.player import Player


class RestRoom(Room):

    def __init__(self, floor=1):
        super().__init__(floor)

        self.room_type = RoomType.REST

        

    def enter(
        self,
        player,
        context
    ):

        heal = int(player.hp_max * 0.3)

        player.hp = min(
            player.hp_max,
            player.hp + heal
        )
        while True:
            print("\nSala de descanso.")
            print(f"Recuperas {heal} HP.")

            print("\n1. Distribuir Stats.")

            print("\n2. Seguir Descendiendo.")

            respuesta = int(input("\n¿Que hacer?: "))
            if respuesta == 1:

                player.distribuir_stats()
            elif respuesta == 2:
                break

        """
        En un futuro aqui se añadiran las opciones para si craftear algo
        o algunas cosas mas para el inventario 
        """


        self.completed = True

