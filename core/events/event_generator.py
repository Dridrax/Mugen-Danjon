import random

from core.events.shrine_event import ShrineEvent
from core.events.healing_event import HealingEvent


def generate_event():

    events = [

        ShrineEvent(),
        HealingEvent()
    ]

    return random.choice(events)