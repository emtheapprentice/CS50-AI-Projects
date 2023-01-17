"""
Tic Tac Toe Player
"""

import math
import copy

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    elif terminal(board) == True:
        return False
    flatboard = sum(board, [])
    Xcount = flatboard.count(X)
    Ocount = flatboard.count(O)
    if Xcount > Ocount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    if terminal(board):
        return False
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                actions.add((row, column))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newstate = copy.deepcopy(board)
    row = action[0]
    col = action[1]
    if newstate[row][col] != EMPTY:
        raise Exception
    else:
        newstate[row][col] = player(board)
        return newstate


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2]:
            if board[row][0] == X:
                return X
            elif board[row][0] == O:
                return O
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == X:
                return X
            elif board[0][col] == O:
                return O
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    elif board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    flatboard = sum(board, [])
    Emptycount = flatboard.count(EMPTY)
    
    if winner(board) != None or Emptycount == 0:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == None:
        return 0
    elif winner(board) == X:
        return 1
    else:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        v = -math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v
    def min_value(board):
        v = math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
    
    if terminal(board):
        return None
    elif player(board) == X:
        top = -math.inf
        for action in actions(board):
            maxvalue = min_value(result(board, action))
            if maxvalue > top:
                top = maxvalue
                optimal = action

    elif player(board) == O:
        top = math.inf
        for action in actions(board):
            minvalue = max_value(result(board, action))
            if minvalue < top:
                top = minvalue
                optimal = action

    return optimal