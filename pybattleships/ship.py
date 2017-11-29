'''
This module defines the class :class:`Ship`, and a helper class,
:class:`ShotResult`.
'''
import enum
import re

from typing import List, Tuple


class ShotResult(enum.IntEnum):
    ''' A ShotResult represents the result of firing on a :class:`Ship`. '''
    MISS = 0 
    ''' Shot did not hit Ship. '''
    HIT = 1
    ''' Shot hit Ship, did not sink yet. '''
    SUNK = 2
    ''' Shot hit Ship, Ship sunk. '''
    LOSS = 3
    ''' Shot hit Ship, Ship sunk, Ship was last Ship on Board. '''

    @property
    def char(self) -> str:
        ''' Return the character to use when pretty-printing. '''
        return ['*', 'X', '#', 'B^u'][self]

class Ship:
    '''
    A Ship represents a Battleship piece.

    '''

    def __init__(self, x: int, y: int, horizontal: bool, size: int):
        '''
        :param int x: The x-coordinate of the top-left square.
        :param int y: The y-coordinate of the top-left square.
        :param bool horizontal: Whether the ship is positioned horizontally
            (True), or vertically (False).
        :param int size: The number of squares the Ship occupies.
        '''
        self._x = x
        self._y = y

        self._horizontal = horizontal # type: bool
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
        '''
        A ship sinks when every position is hit, which means it has been hit
        `size` times. Once the ship has sunk, this property is True.

        :type: bool
        '''
        return self._hit >= self._size

    @property
    def fields(self) -> List[Tuple[int, int]]:
        '''
        Return the list of fields this Ship occupies as a list of (x, y)
        tuples.

        :type: List[Tuple[int, int]]
        '''
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
        '''
        Assert that the given shot was on this Ship, if so, increase the
        hitcounter. Return whether the Ship was missed, hit, or sunk.
        '''

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
        '''
        Return the number of fields the Ship occupies.

        :type: int
        '''
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

    @staticmethod
    def parse_notation(notation: str):
        '''
        Parse a written representation of a Ship, like `(A1, h, 2)`,
        return a new Ship on this position.
        '''

        match = cls.notational_regex.match(notation)

        if not match:
            raise ValueError("Invalid notation!")

        x = ord(match.group('x').upper()) - ord('A')
        y = int(match.group('y'))         - 1

        horizontal = match.group('orientation').upper() == 'H'

        size = int(match.group('size'))

        return Ship(x, y, horizontal, size)

    def __repr__(self):
        return '<Ship({}, {}, {}, {})>'.format(self._x, self._y,
                self._horizontal, self._size)
