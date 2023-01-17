import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

board = initial_state()

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    elif terminal(board) == True:
        return False
    Xcount = board.count(X)
    Ocount = board.count(O)
    if Xcount > Ocount:
        return O
    else:
        return X

flatlist = sum(board, [])

print(flatlist.count(EMPTY))
