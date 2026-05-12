
class DungeonContext:

    def __init__(self):

        self.current_floor = 1
        self.current_room = 1
        self.room_history = []

        self.total_rooms = 0

        self.gold = 0

        self.tension = 0

        self.rooms_cleared = 0

        self.flags = {}