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
    if terminal(board):
        return O
    
    countfilled = 0
    for row in board:
        for item in row:
            if item is not EMPTY:
                countfilled+=1

    if countfilled%2 == 0:
        return X
    
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return (0,0)
    
    possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                possible.add((i,j))

    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    saveboard = copy.deepcopy(board)
    saveboard[action[0]][action[1]] = player(board)
    return saveboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []

    for i in range(3):
        lines.append(board[i])
        lines.append([board[0][i], board[1][i], board[2][i]])

    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line.count(line[0]) == 3 and line[0] is not None:
            return line[0]
        
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) is not None):
        return True
    
    countfilled = 0
    for row in board:
        for item in row:
            if item is not EMPTY:
                countfilled+=1

    if countfilled == 9:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if(winner(board) is None):
        return 0
    if(winner(board) == X):
        return 1
    return -1

def minimax(board):

    """
    Returns the optimal action for the current player on the board.
    """

    if(terminal(board)):
        return None
    
    current = player(board)
    if current == X:
        _, action = max_value(board)
        return action
    else:
        _, action = min_value(board)
        return action

    
def max_value(board):
        
        if terminal(board):
            return utility(board), None
        
        v = -2
        best_action = None

        for action in actions(board):
            minv, _ = min_value(result(board, action))
            if minv > v:
                v = minv
                best_action = action
                if v == 1:
                    break
        return v, best_action


def min_value(board):
        
        if terminal(board):
            return utility(board), None
        
        v = 2
        best_action = None

        for action in actions(board):
            maxv, _ = max_value(result(board, action))
            if maxv < v:
                v = maxv
                best_action = action
                if v == -1:
                    break
        return v, best_action