import copy
import math

"""
Tic Tac Toe Player
"""

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
    x_sum = 0
    o_sum = 0

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == "X":
                x_sum += 1

            if board[i][j] == "O":
                o_sum += 1

    if x_sum > o_sum:
        return O

    if x_sum == o_sum:
        return X

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    s = set()

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                tmp = (i, j)
                s.add(tmp)

    return s


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    if board[i][j] != EMPTY:
        raise Exception("Invalid Action!!!")

    else:
        deep_copy = copy.deepcopy(board)
        chance = player(board)
        if chance == X:
            deep_copy[i][j] = X

        elif chance == O:
            deep_copy[i][j] = O

        return deep_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = None
    i = 0

    for j in range(0, 3):
        if board[j][i] == board[j][i + 1] == board[j][i + 2]:
            if board[j][i] != EMPTY:
                win = board[j][i]

        elif board[i][j] == board[i + 1][j] == board[i + 2][j]:
            if board[i][j] != EMPTY:
                win = board[i][j]

        elif board[0][0] == board[1][1] == board[2][2]:
            if board[1][1] != EMPTY:
                win = board[1][1]

        elif board[2][0] == board[1][1] == board[0][2]:
            if board[1][1] != EMPTY:
                win = board[1][1]
    return win


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True

    elif winner(board) == O:
        return True

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1

    if winner(board) == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    maxx = float('-inf')
    minn = float('inf')

    if player(board) == X:
        # X is trying to maximise score
        return max_value(board, maxx, minn)[1]

    else:
        # O is trying to minimise score
        return min_value(board, maxx, minn)[1]


def max_value(board, maxx, minn):
    move = None
    if terminal(board):
        return [utility(board), None]
    v = float('-inf')
    for action in actions(board):
        test = min_value(result(board, action), maxx, minn)[0]
        maxx = max(maxx, test)
        if test > v:
            v = test
            move = action
        if maxx >= minn:
            break
    return [v, move]


def min_value(board, maxx, minn):
    move = None
    if terminal(board):
        return [utility(board), None]
    v = float('inf')
    for action in actions(board):
        test = max_value(result(board, action), maxx, minn)[0]
        minn = min(minn, test)
        if test < v:
            v = test
            move = action
        if maxx >= minn:
            break
    return [v, move]
