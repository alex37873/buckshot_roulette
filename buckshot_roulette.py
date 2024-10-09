from enum import Enum
from random import choices, randint, random, shuffle
from typing import List


class Item(Enum):
    ADRENALINE = 0
    BEER = 1
    BURNER_PHONE = 2
    CIGARETTE_PACK = 3
    EXPIRED_MEDICINE = 4
    HAND_SAW = 5
    HANDCUFFS = 6
    INVERTER = 7
    MAGNIFYING_GLASS = 8


class Shell(Enum):
    BLANK = 0
    LIVE = 1


class Player:
    def __init__(
        self, name: str = "Player", health: int = 2, items: List[Item] = None
    ) -> None:
        self.name = name
        self.health = health
        self.items = list() if items is None else items
        self.is_handcuffed = False

    def __str__(self) -> str:
        return f"""Player ({self.name})"""

    def __repr__(self) -> str:
        item_names = ", ".join(item.name for item in self.items)
        return f"""Player — {self.__hash__()} (Name: {self.name}; Health: {self.health}; Items: {item_names or 'None'})"""


class Game:
    def __init__(self, max_health: int = 2, max_shells: int = 8) -> None:
        self.max_health = max_health
        self.max_shells = max_shells
        self.current_player = None
        self.turn = 0
        self.round = 0
        self.damage = 1
        self.shells = choices(
            population=[Shell.BLANK, Shell.LIVE],
            weights=(0.5, 0.5),
            k=max_shells,
        )
        print(
            f"""Shells: {', '.join([shell.name for shell in self.shells])}""")
        shuffle(x=self.shells)

    def add_items(self, player: Player, items: List[Item]) -> None:
        player.items.extend(items)

    def remove_item(self, player: Player, item: Item) -> None:
        match item:
            case Item.HAND_SAW:
                self.damage = 1

        player.items.remove(item)

    def use_item(self, player: Player, item: Item) -> None:
        match item:
            case Item.ADRENALINE:
                pass

            case Item.BEER:
                if self.shells:
                    del self.shells[0]

            case Item.BURNER_PHONE:
                if self.shells:
                    if len(self.shells) == 1:
                        print("""How unfortunate...""")

                    random_shell_index = randint(
                        a=0,
                        b=len(self.shells) - self.turn - 1,
                    )
                    print(
                        f"""{random_shell_index + 1} shell ... {self.shells[random_shell_index].name}"""
                    )

            case Item.CIGARETTE_PACK:
                if player.health + 1 <= self.max_health:
                    player.health += 1

            case Item.EXPIRED_MEDICINE:
                if random() < 0.5:
                    player.health -= 1
                else:
                    if player.health + 2 <= self.max_health:
                        player.health += 2
                    elif player.health + 1 <= self.max_health:
                        player.health += 1

            case Item.HAND_SAW:
                self.damage = 2

            case Item.HANDCUFFS:
                pass

            case Item.INVERTER:
                if self.shells:
                    self.shells[0] = (
                        Shell.BLANK if self.shells[0] == Shell.LIVE else Shell.LIVE
                    )

            case Item.MAGNIFYING_GLASS:
                if self.shells:
                    print(f"""{self.shells[0].name}""")

        self.remove_item(player=player, item=item)

    def use_shotgun(self, player: Player) -> None:
        if self.shells:
            if self.shells[0] == Shell.LIVE:
                player.health -= 1
            del self.shells[0]


if __name__ == "__main__":
    game = Game()

    dealer = Player(
        name="Dealer",
        health=game.max_health,
        items=[
            Item.MAGNIFYING_GLASS,
            Item.BURNER_PHONE,
            Item.INVERTER,
            Item.MAGNIFYING_GLASS,
            Item.BEER,
            Item.MAGNIFYING_GLASS,
        ],
    )

    game.current_player = dealer

    print(repr(dealer))

    game.use_item(player=dealer, item=Item.MAGNIFYING_GLASS)
    game.use_item(player=dealer, item=Item.INVERTER)
    game.use_item(player=dealer, item=Item.MAGNIFYING_GLASS)
    game.use_item(player=dealer, item=Item.BEER)
    game.use_item(player=dealer, item=Item.MAGNIFYING_GLASS)

    print(repr(dealer))
