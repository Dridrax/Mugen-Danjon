from core.dungeon.rooms.room import Room
from core.dungeon.rooms.room_types import RoomType


class EventRoom(Room):

    def __init__(self, floor, event):

        super().__init__(floor)

        self.room_type = RoomType.EVENT

        self.event = event

    def enter(self, player, context):

        print("\nHas encontrado una sala de evento.")

        self.event.run(player, context)

        self.completed = True