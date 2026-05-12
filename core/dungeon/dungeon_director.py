import random

from core.dungeon.rooms.room_types import RoomType

from core.ia.director_utilidad import (
    score_combat,
    score_rest,
    score_event
)

class DungeonDirector:

    def choose_room_type(
        self,
        context,
        history
    ):

        scores = {
        
            RoomType.COMBAT:
                score_combat(
                    context,
                    history
                ),
        
            RoomType.REST:
                score_rest(
                    context,
                    history
                ),
        
            RoomType.EVENT:
                score_event(
                    context,
                    history
                )
        }

        return self.weighted_choice(scores)
    
    def weighted_choice(self, scores):
    
        total = sum(scores.values())
    
        roll = random.uniform(0, total)
    
        current = 0
    
        for room_type, score in scores.items():
        
            current += score
    
            if roll <= current:
                return room_type
    
        return RoomType.COMBAT
    
    def generate_floor_plan(self, context):

        floor_plan = []

        total_rooms = 6

        simulated_history = []

        for i in range(total_rooms - 1):

            room_type = self.choose_room_type(
                context,
                simulated_history
            )

            floor_plan.append(room_type)

            simulated_history.append(room_type)

        floor_plan.append(RoomType.BOSS)

        return floor_plan