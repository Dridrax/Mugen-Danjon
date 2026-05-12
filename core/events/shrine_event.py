from core.events.event import Event


class ShrineEvent(Event):

    def run(self, player, context):

        print("\nEncuentras un altar antiguo.")

        print("1. Rezar")
        print("2. Ignorar")

        choice = input("> ")

        if choice == "1":

            hp_cost = 10
            attack_bonus = 2

            player.hp = max(
                1,
                player.hp - hp_cost
            )

            player.ataque_base += attack_bonus

            print(
                f"\nPierdes {hp_cost} HP."
            )

            print(
                f"Ganas +{attack_bonus} ataque."
            )

        else:

            print(
                "\nDecides ignorar el altar."
            )