class GameState:
    def __init__(self, board, players, max_rounds_num=20):
        self._players = players
        self._max_rounds_num = max_rounds_num
        self._board = board
        self._current_player = self._players[0]
        self._winner = None

    def move_pawn(self):
        pass

    def prepare_game(self):
        pass

    def make_move(self):
        pass
