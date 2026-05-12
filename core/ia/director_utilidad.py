from core.dungeon.rooms.room_types import RoomType


def score_combat(context, history):

    score = 0.7

    hp_ratio = (
        context.player.hp /
        context.player.hp_max
    )

    # Más vida = más combate
    score += hp_ratio * 0.2

    # Penalizar repetición
    recent_rooms = history[-3:]

    combat_count = recent_rooms.count(
        RoomType.COMBAT
    )

    score -= combat_count * 0.15

    return max(score, 0)


def score_rest(context, history):

    hp_ratio = (
        context.player.hp /
        context.player.hp_max
    )

    missing_hp = 1.0 - hp_ratio

    score = missing_hp * 0.9

    recent_rooms = history[-2:]

    rest_count = recent_rooms.count(
        RoomType.REST
    )

    # Evitar spam descanso
    score -= rest_count * 0.4

    return max(score, 0)


def score_event(context, history):

    score = 0.35

    recent_rooms = history[-3:]

    combat_count = recent_rooms.count(
        RoomType.COMBAT
    )

    # Más combates recientes = más eventos
    score += combat_count * 0.1

    return max(score, 0)

def score_boss(context):

    score = 0.06

    if context.room_history == RoomType.COMBAT:
        pass
