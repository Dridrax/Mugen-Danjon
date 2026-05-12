from enum import Enum


class RoomType(Enum):

    COMBAT = "combat"
    REST = "rest"
    EVENT = "event"
    ELITE = "elite"
    BOSS = "boss"
    TREASURE = "treasure"
    MERCHANT = "merchant"
    TRAP = "trap"