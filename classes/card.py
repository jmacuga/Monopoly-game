from classes.game_constants import ChanceFieldAction
from classes.player import Player


class ChanceCard:
    def __init__(self,
                 card_id: int,
                 description: str,
                 action: ChanceFieldAction,
                 money: int):
        self._card_id = card_id
        self._description = description
        self._action = action
        self._money = money

    def card_id(self):
        return self._card_id

    def description(self):
        return self._description

    def action(self):
        return self._action

    def money(self):
        return self._money

    def __str__(self):
        return self._description

    def use_card(self, player: Player):
        if self._action == ChanceFieldAction.PAY.value:
            player.spend_money(self.money())
        elif self._action == ChanceFieldAction.EARN.value:
            player.earn_money(self.money())
