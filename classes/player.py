class Player:
    max_id = 0

    def __init__(self, name, player_id) -> None:
        self.player_id = Player.max_id
        Player.max_id += 1
        self.name = name
        self.owned_property_fields = {}
        self.current_dice_roll_sum
        self.is_in_jail = False
        self.money
        self.current_position

    def move_pawn():
        pass

    def buy_property(self, board):
        pass
