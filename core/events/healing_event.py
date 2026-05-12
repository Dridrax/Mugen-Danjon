from core.events.event import Event


class HealingEvent(Event):

    def run(self, player, context):

        print("\nEncuentras una fuente curativa.")

        heal = int(player.hp_max * 0.4)

        player.hp = min(
            player.hp_max,
            player.hp + heal
        )

        print(
            f"Recuperas {heal} HP."
        )