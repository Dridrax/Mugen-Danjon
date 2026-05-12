from core.dungeon.rooms.room_types import RoomType

from core.dungeon.rooms.combat_room import CombatRoom
from core.dungeon.rooms.rest_room import RestRoom
from core.dungeon.rooms.boss_room import BossRoom
from core.dungeon.rooms.event_room import EventRoom

from core.events.event_generator import (
    generate_event
)

from core.generador_enemigos import (
    generar_encuentro,
    generar_boss
)

class DungeonGenerator:

    def generate_room(
            self,
            room_type,
            floor_number
    ):

        if room_type == RoomType.COMBAT:

            enemies = generar_encuentro(floor_number)

            return CombatRoom(
                floor=floor_number,
                enemies=enemies
            )
        
        elif room_type == RoomType.REST:

            return RestRoom(
                floor=floor_number,
            )
        
        elif room_type == RoomType.BOSS:

            boss = generar_boss(floor_number)

            return BossRoom(
                floor=floor_number,
                boss=boss
            )
        
        elif room_type == RoomType.EVENT:
        
            event = generate_event()
        
            return EventRoom(
                floor=floor_number,
                event=event
            )
        
        
        raise ValueError(
            f"RoomType no soportado: {room_type}"
        )