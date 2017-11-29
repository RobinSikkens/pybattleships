'''
Defines the Game.
'''
from bottleships.board import Board
from bottleships.ship import Ship, ShotResult

class Game:
    def __init__(self, player1, player2):
        # 2x board
        # 2x player
        # turn-tracker
        self.turn = 0
        self.player1 = player1
        self.player2 = player2

        self.players = {
            player1: 1,
            player2: 2,
            1: player1,
            0: player2
        }

        self.boards = {
            player1: None,
            player2: None
        }

    def setup_board(self, player_id: str, ships : [Ship]) -> bool:
        ''' Create a board from the given set of ships, assert validity and
        register the Board with the Game if it is valid. '''

        try:
            board = Board(ships)
        except ValueError:
            # Board invalid, abort
            return False

        assert player_id in self.boards

        self.boards[player_id] = board
        return True

    def start_game(self) -> bool:
        ''' Assert both boards are present and valid, set turn-tracker to 1,
        give turn to player 1. '''

        for player, board in self.boards.items():
            if not (board and board.valid_board):
                return False

        self.turn = 1
        return True

    @property
    def current_player(self) -> str:
        if self.turn == 0:
            return None

        return self.players[self.turn % 2]

    @property
    def current_adversary(self) -> str:
        if self.turn == 0:
            return None

        return self.players[(self.turn + 1) % 2]

    def process_fire(self, x, y) -> ShotResult:
        player_id = self.current_adversary
        board = self.boards[player_id]
        result = board.process_hit(x, y)
        self.turn += 1

        if result == ShotResult.SUNK and board.is_loss:
            return ShotResult.LOSS

        return result
