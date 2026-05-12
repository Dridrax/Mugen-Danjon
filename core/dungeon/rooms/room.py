from core.dungeon.rooms.room_types import RoomType


class Room:

    def __init__(self, floor=1):

        self.floor = floor
        self.completed = False

    def enter(
        self,
        player,
        context
    ):
        raise NotImplementedError