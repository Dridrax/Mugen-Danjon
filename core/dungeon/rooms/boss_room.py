from core.dungeon.rooms.room import Room
from core.dungeon.rooms.room_types import RoomType

from core.combate import Combate


class BossRoom(Room):

    def __init__(self, floor, boss):

        super().__init__(floor)

        self.room_type = RoomType.BOSS

        self.boss = boss

    def enter(
        self,
        player,
        context
    ):

        print("\n¡Has entrado en la sala del BOSS!")

        combate = Combate(
            jugador=player,
            enemigos=[self.boss],
            floor_number=context.current_floor,
            room_number=context.current_room,
            total_rooms=context.total_rooms
        )

        combate.iniciar()

        if player.hp > 0:
            context.rooms_cleared += 1

        self.completed = True