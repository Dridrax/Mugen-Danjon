from core.dungeon.rooms.room import Room
from core.dungeon.rooms.room_types import RoomType

from core.combate import Combate


class CombatRoom(Room):

    def __init__(self, floor, enemies):

        super().__init__(floor)

        self.room_type = RoomType.COMBAT

        self.enemies = enemies
        

    def enter(
        self,
        player,
        context
    ):

        print("\nEntrando en sala de combate.")

        combate = Combate(
            jugador=player,
            enemigos=self.enemies,
            floor_number=context.current_floor,
            room_number=context.current_room,
            total_rooms=context.total_rooms
        )

        combate.iniciar()

        if player.hp > 0:

            context.rooms_cleared += 1

            from core.rewards.reward_generator import generate_reward

            reward = generate_reward()

            reward.apply(player)

        self.completed = True