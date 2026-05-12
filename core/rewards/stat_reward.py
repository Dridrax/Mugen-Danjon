from core.rewards.reward import Reward

class StatReward(Reward):

    def __init__(self, stat, amount):

        self.stat = stat
        self.amount = amount
    
    def apply(self, player):
        
        if self.stat == "hp_max":

            player.hp_max += self.amount
            player.hp += self.amount

            print(f"\nMAX HP aumentado en {self.amount}.")

        elif self.stat == "ataque_base":

            player.ataque_base += self.amount

            print(f"\nATAQUE aumentado en {self.amount}.")