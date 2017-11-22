'''
Defines a Ship, which is placed on a Board.
'''
import enum
import re


class ShotResult(enum.IntEnum):
    MISS = 0
    HIT = 1
    SUNK = 2

    @property
    def char(self):
        return ['*', 'X', '#'][self]

class Ship:
    '''
    A Ship represents a Battleship piece.
    '''

    def __init__(self, x: int, y: int, horizontal: bool, size: int) -> None:
        ''' Instantiate a new Ship. '''
        self._x = x
        self._y = y
        self._horizontal = horizontal
        self._size = size

        self._hit = 0

        # Check boundaries
        if (horizontal and x+size-1 >= 10) or (not horizontal and y+size-1 >= 10) \
            or x < 0 or y < 0:
            raise ValueError(
                "Can't place a Ship outside of the board: {}, {}".format(
                    x+size, y)
                )

        if size <= 1 or size > 5:
            raise ValueError("Ship size outside [2..5]: {}".format(size))

    @property
    def sunk(self) -> bool:
        ''' A ship sinks when every position is hit, which means it has been
        hit `size` times. '''
        return self._hit >= self._size

    @property
    def fields(self) -> [(int, int)]:
        ''' Return the list of fields this Ship occupies. '''
        pos_x, pos_y = self._x, self._y
        result = [(pos_x, pos_y)]

        if self._horizontal:
            deltax = 1 # Go left
            deltay = 0
        else:
            deltax = 0
            deltay = 1 # Go down

        for i in range(self._size-1):
            pos_x += deltax
            pos_y += deltay

            result.append( (pos_x, pos_y) )

        return result

    def process_hit(self, x: int, y: int) -> ShotResult:
        ''' Assert that the given shot was on this ship, if so, increase the
        hitcounter. '''

        if (self._horizontal and \
            y == self._y and x >= self._x and x < self._x + self._size) \
           or (not self._horizontal and \
            x == self._x and y >= self._y and y < self._y + self._size):

            self._hit += 1
            if self.sunk:
                return ShotResult.SUNK
            return ShotResult.HIT

        return ShotResult.MISS

    @property
    def size(self):
        return self._size

    notational_pattern = r'''
\(
(?P<x>[A-Ja-j])
(?P<y>([1-9]|10)),\s*
(?P<orientation>[hHvV]),\s*
(?P<size>[2-5])
\)
    '''
    notational_regex = re.compile(notational_pattern, re.X)
    @classmethod
    def parse_notation(cls, notation: str):
        ''' Parse a written representation of the Board like `(A1, h, 2)`. '''
        match = cls.notational_regex.match(notation)

        if not match:
            raise ValueError("Git gud")

        x = ord(match.group('x').upper()) - ord('A')
        y = int(match.group('y'))         - 1

        horizontal = match.group('orientation').upper() == 'H'

        size = int(match.group('size'))

        return Ship(x, y, horizontal, size)

    def __repr__(self):
        return '<Ship({}, {}, {}, {})>'.format(self._x, self._y,
                self._horizontal, self._size)
