import random

from core.rewards.stat_reward import StatReward

def generate_reward():

    rewards = [
        StatReward("hp_max", 5),
        StatReward("ataque_base", 1)
    ]

    return random.choice(rewards)