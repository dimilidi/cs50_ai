"""
Tic Tac Toe Player
"""

import copy
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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # No more turns if the game is over (either someone has won or the board is full)
    if terminal(board):
        return "Game is over"
    else:
        # Determine whose turn it is:
        # If X and O are equal or O has fewer moves, it's X's turn (X starts the game).
        # If X has more moves, it's O's turn.
        x_count = sum(row.count(X) for row in board)
        o_count = sum(row.count(O) for row in board)
        return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    # Iterate over rows
    for i in range(len(board)):
        # Iterate over columns
        for j in range(len(board[i])):
            # Check if the cell is empty
            if board[i][j] == EMPTY:
                # Add the position as a tuple to the set
                actions_set.add((i, j))

    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Added check to ensure action is a tuple (i, j)
    if not isinstance(action, tuple) or len(action) != 2:
        raise ValueError(f"Action {action} is not a valid tuple (i, j).")

    # Unpack the action
    (i, j) = action

    # Check if the action is within bounds
    if i < 0 or i >= len(board) or j < 0 or j >= len(board[i]):
        raise ValueError(f"Action {action} is out of bounds.")

    # Check if the cell is already occupied
    if board[i][j] != EMPTY:
        raise ValueError(f"Cell {action} is already occupied.")

    # Determine the player to move
    current_player = player(board)

    # Deep copy of the board
    board_copy = copy.deepcopy(board)

    # Make the move
    board_copy[i][j] = current_player

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows for a win
    for row in board:
        if row.count(O) == 3:
            return O
        if row.count(X) == 3:
            return X

    # Check columns for a win
    for col in range(len(board)):
        is_column_O = True
        is_column_X = True
        for row in range(len(board)):
            if board[row][col] != O:
                is_column_O = False
            if board[row][col] != X:
                is_column_X = False
        if is_column_O:
            return O
        if is_column_X:
            return X

    # Check diagonals for a win
    if all(board[i][i] == O for i in range(len(board))):
        return O
    if all(board[i][i] == X for i in range(len(board))):
        return X
    if all(board[i][len(board) - 1 - i] == O for i in range(len(board))):
        return O
    if all(board[i][len(board) - 1 - i] == X for i in range(len(board))):
        return X

    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    total_moves = sum(row.count(X) + row.count(O) for row in board)
    # game is over when there is a winner or when all fields are filled out with no winner
    return total_moves == 9 or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)

    match game_winner:
        case "X":
            return 1
        case "O":
            return -1
        case _:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the game is over, no action can be made
    if terminal(board):
        return None

    # Get the current player (X or O)
    current_player = player(board)

    if current_player == X:
        return max_value(board)[1]
    elif current_player == O:
        return min_value(board)[1]


def max_value(board):
    """
    Returns maximum possible value and the corresponding action for player X.
    """
    # If the game is over, return the utility of the current board and no move
    if terminal(board):
        return utility(board), None

    # Initialize the value to negative infinity
    v = float('-inf')
    best_move = None

    # Get all the possible actions (i, j) on the board
    all_actions = actions(board)

    # Iterate over each possible action and recursively call min_value for the resulting board
    for action in all_actions:
        # Call min_value for each action and get the corresponding value and action
        move_value = min_value(result(board, action))[0]
        if move_value > v:
            v = move_value
            best_move = action

    # Return the best value and corresponding action
    return v, best_move


def min_value(board):
    """
    Returns minimum possible value from all the valid actions for the minimizer (player O).
    """
    # If the game is over, return the utility of the current board and no move
    if terminal(board):
        return utility(board), None

    # Initialize the value to positive infinity
    v = float('inf')
    best_move = None

    # Get all the possible actions (i, j) on the board
    all_actions = actions(board)

    for action in all_actions:
        # Call max_value for each action and get the corresponding value and action
        move_value = max_value(result(board, action))[0]
        if move_value < v:
            v = move_value
            best_move = action

    # Return the best value and corresponding action
    return v, best_move
