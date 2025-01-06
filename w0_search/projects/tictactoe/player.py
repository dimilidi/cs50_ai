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




board = [
    [O, O, X],
    [O, X, EMPTY],
    [O, O, X]
]


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

print("Winner -",winner(board))


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    total_moves = sum(row.count(X) + row.count(O) for row in board)
    # game is over when there is a winner or when all fields are filled out with no winner
    return total_moves == 9 or winner(board) is not None


print("Terminal: ",terminal(board))



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



print(player(board) )




def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
         return None

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



print(actions(board))

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

print("Utility: ", utility(board)) 


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Deep copy of the board
    board_copy = copy.deepcopy(board)

    # Unpack the action
    i, j = action

    # Check if the action is within bounds
    if i < 0 or i >= len(board) or j < 0 or j >= len(board[i]):
        raise ValueError(f"Action {action} is out of bounds.")

    # Check if the cell is already occupied
    if board[i][j] != EMPTY:
        raise ValueError(f"Cell {action} is already occupied.")
    
    # Determine the player to move
    current_player = player(board)

    # Make the move
    board_copy[i][j] = current_player

    return board_copy





MAX = float('inf')
MIN = float('-inf')

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
        return min_value(board)
    elif current_player == O:
        return min_value(board)


def max_value(board):
     """
    Returns maximum possible value from all the valid actions for the maximizer (player X).

    """
    if terminal(board):
        return utility(board)
    # Initialize the value to negative infinity.
    v = MIN
     # Get all the possible actions (i, j) on the board.
    all_actions = actions(board)

    for action in all_actions:
        #  Maximizing for player X
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    """
    Returns minimum possible value from all the valid actions for the minimizer (player O).

    """
    # Initialize the value to positive infinity.
    v = MAX
    # Get all the possible actions (i, j) on the board.
    all_actions = actions(board)

    for action in all_actions:
        # Minimizing for player O after applying the action and maximizing the opponent's moves
        v = min(v, max_value(result(board, action)))
    return v
