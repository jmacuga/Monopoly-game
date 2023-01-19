from enum import Enum
from classes.player import Player


class ChanceFieldAction(Enum):
    """Actions available when using chance cards."""
    PAY = 'pay'
    EARN = 'earn'


def chance_action_values():
    return [act.value for act in ChanceFieldAction]


class ActionError(Exception):
    """Raised when action error is not valid"""
    pass


class ChanceCard:
    """Chance card that can be randomly selected from chance card in the board.

    Attributes
    ----------

    _card_id : int
        Card index.
    _description : str
        Short card description shown to the player.
    _action : str
        Type of action that is performed when card is used.
        Available actions are the values od ChanceFieldAction enum.
    _money : int
        The amount of money that is taken from or given to the player.
    """

    def __init__(self,
                 card_id: int,
                 description: str,
                 action: str,
                 money: int = None):
        """Initates field attributes

        Parameters
        ----------
        card_id : int
            Card index.
        description : str
            Short card description shown to the player.
        action : str
            Type of action that is performed when card is used.
            Available actions are the values od ChanceFieldAction enum.
        money : int, optional
            The amount of money that is taken from or given to the player.

        Raises
        ------
        ActionError
            If the action is not in ChanceFieldAction enum values.
        """
        self._card_id = card_id
        self._description = description
        if action not in chance_action_values():
            raise ActionError("Provided action is ot available")
        self._action = action
        self._money = money

    def card_id(self) -> int:
        """Gets card id."""
        return self._card_id

    def description(self) -> str:
        """Gets the title of the card that is shown to the player."""
        return self._description

    def action(self) -> ChanceFieldAction:
        """Gets the card's action"""
        return self._action

    def money(self):
        """Gets the amound of money included in card action."""
        return self._money

    def __str__(self):
        """Gets the card description."""
        return self._description

    def use_card(self, player: Player):
        """Performs the cards' action.

        Parameters
        ----------
        player : pLayer
            The player who chose teh card.
        """
        if self._action == ChanceFieldAction.PAY.value:
            player.spend_money(self.money())
        elif self._action == ChanceFieldAction.EARN.value:
            player.earn_money(self.money())
