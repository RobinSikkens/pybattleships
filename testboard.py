from bottleships.ship import Ship, ShotResult
from bottleships.board import Board

#s = Ship.parse_notation('(B3, H, 3)')
#fields = s.fields

#for field in s.fields:
    #print(s.process_hit(*field)) # Get noscoped!!!11!!

s1  = Ship.parse_notation('(A1, H, 2)')
s2  = Ship.parse_notation('(D1, V, 3)')
s3  = Ship.parse_notation('(G1, H, 4)')
s4  = Ship.parse_notation('(A3, V, 4)')
s5  = Ship.parse_notation('(F3, H, 3)')
s6  = Ship.parse_notation('(J3, V, 2)')
s7  = Ship.parse_notation('(F6, V, 2)')
s8  = Ship.parse_notation('(J6, V, 3)')
s9  = Ship.parse_notation('(E10, H, 5)')
s10 = Ship.parse_notation('(A8, H, 2)')

ships = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]

board = Board(ships)

shots = [
    (2, 3),
    (5, 4),
    (6, 4),
    (1, 5),
    (7, 5),
    (9, 5),
    (3, 6),
    (9, 6),
    (0, 7),
    (1, 7),
    (7, 7),
]

for shot in shots:
    board.process_hit(*shot)
