from core.dungeon.dungeon_generator import DungeonGenerator
from core.dungeon.dungeon_context import DungeonContext
from core.dungeon.dungeon_director import DungeonDirector


class DungeonRun:

    def __init__(self, player):

        self.player = player

        self.context = DungeonContext()

        self.context.player = player

        self.generator = DungeonGenerator()

        self.director = DungeonDirector()

        self.rooms = []

        self.is_active = True

    def start(self):

        print("Comienza la aventura.")

        self.generate_floor()

        while self.is_active:
            self.process_current_room()

    def generate_floor(self):

        floor_plan = self.director.generate_floor_plan(
            self.context
        )

        self.rooms = []

        for room_type in floor_plan:

            room = self.generator.generate_room(
                room_type=room_type,
                floor_number=self.context.current_floor
            )

            self.rooms.append(room)

        self.context.current_room = 1

        self.context.total_rooms = len(self.rooms)

    def process_current_room(self):

        room_index = self.context.current_room - 1

        room = self.rooms[room_index]

        room.enter(
            player=self.player,
            context=self.context
            )
        
        self.context.room_history.append(
            room.room_type
        )

        if self.player.hp <= 0:
            self.game_over()
            return

        self.context.current_room += 1

        if self.context.current_room > len(self.rooms):
            self.next_floor()

    def next_floor(self):

        self.context.current_floor += 1

        print(f"\nSubes al piso {self.context.current_floor}")

        self.generate_floor()

    def game_over(self):

        print("\nHas muerto.")

        self.is_active = False