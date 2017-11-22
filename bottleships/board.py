''' Defines a Board, which represents one player's half of the game. '''
from collections import OrderedDict
from itertools import dropwhile

from .ship import ShotResult, Ship


class Board:
    ''' Represents one half of the game. '''
    def __init__(self, ships : [Ship]) -> None:
        self._tries = OrderedDict() # type: [(int, int)] : ShotResult

        self._ships = ships

        if not self.valid_board:
            print('invalid!!!!')

    @property
    def valid_board(self) -> bool:
        if len(self._ships) < 10:
            return False

        fields = []
        for ship in self._ships:
            fields += ship.fields

        if len(fields) != len(set(fields)):
            return False

        correct = [2, 2, 2, 2, 3, 3, 3, 4, 4, 5]
        actual = list(map(lambda x: x.size, self._ships))

        if sorted(actual) != correct:
            return False

        return True

    def process_hit(self, x: int, y: int) -> ShotResult:
        if (x, y) in self._tries:
            return self._tries((x, y))

        results = []
        for ship in self._ships:
            results.append(ship.process_hit(x, y))

        theresult = ShotResult.MISS

        hit_ship = list(dropwhile(lambda x: x == ShotResult.MISS, results))
        if hit_ship:
            theresult = hit_ship[0]

        self._tries[(x, y)] = theresult
        return theresult

    def __repr__(self) -> str:
        return self.prettyprint()

    def prettyprint(self, blind: bool = False) -> str:
        result = [10*['~'] for _ in range(10)]

        if not blind:
            for index, ship in enumerate(self._ships):
                for x, y in ship.fields:
                    result[y][x] = str(index)

        for shot, sresult in self._tries.items():
            x, y = shot
            result[y][x] = sresult.char
        return '\n'.join([''.join(row) for row in result])
