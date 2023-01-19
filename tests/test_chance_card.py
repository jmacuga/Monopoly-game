from classes.chance_card import ChanceCard, ChanceFieldAction, ActionError
from classes.player import Player
import pytest


def test_chance_card_pay():
    card = ChanceCard(card_id=0, description="School tax",
                      action=ChanceFieldAction.PAY.value, money=150)
    player = Player()
    init_money = 1500
    player._money = init_money
    card.use_card(player=player)
    assert player.money() == init_money - card.money()


def test_chance_card_earn():
    card = ChanceCard(card_id=0, description="School tax",
                      action=ChanceFieldAction.EARN.value, money=150)
    player = Player()
    init_money = 1500
    player._money = init_money
    card.use_card(player=player)
    assert player.money() == init_money + card.money()


def test_chance_card_invalid_action():
    with pytest.raises(ActionError):
        ChanceCard(card_id=0, description="School tax",
                   action="bancrupt", money=150)


def test_chance_card_description():
    card = ChanceCard(card_id=0, description="School tax",
                      action=ChanceFieldAction.EARN.value, money=150)
    assert card.description() == "School tax"
