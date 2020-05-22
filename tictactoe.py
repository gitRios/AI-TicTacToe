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
    cont_X = 0
    cont_O = 0

    for row in board:
        for cell in row:
            if cell == X: cont_X += 1
            elif cell == O: cont_O += 1

    if cont_X == cont_O: return X
    else: return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    # Searching for EMPTY cells
    for row_id, row_list in enumerate(board):
        for cell_id in range(len(row_list)):
            if row_list[cell_id] == EMPTY: actions.add((row_id, cell_id))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    # Validating the action
    if len(action) != 2 or max(action) > 2 or min(action) < 0:
        raise Exception("Ação Inválida")

   
    # Copying the old board to new one. (no references to each other)
    new_board = copy.deepcopy(board)

    # Add the action into the new board
    new_board[action[0]][action[1]] = player(board)

    return new_board




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Lines
    for row in board:
        if len(set(row)) == 1 and row[0] != EMPTY:
            return row[0]

    # Diagonal 
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    
    # Inverted Diagonal
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != EMPTY:
        return board[2][0]

    # Colunms
    for colunm in range(3):
        if board[0][colunm] == board[1][colunm] == board[2][colunm] and board[0][colunm] != EMPTY:
            return board[0][colunm]

    # Tie or Game not finished yet
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Winner is not None - Game Over
    if winner(board) != None:
        return True
    
    # Verify EMPTY cells - Game Continue
    for row in board:
        for cell in row:
            if cell == EMPTY: return False

    # Tie - Game over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    #Assuming utility will only be called on a board if terminal(board) is True
    winner_values = {"X": 1, "O": -1}

    # X or O Won
    if winner(board) != None:
        return winner_values[winner(board)]
    
    # Tie
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If the board is a terminal board, the minimax function should return None.
    if terminal(board):
        return None

    actual_player = player(board)
    actions_values = {}
    
    # X aims to maximize the score
    if actual_player == X:
        v = - math.inf
        for action in actions(board):
            action_value = min_value(result(board,action))
            actions_values[action_value] = action
            v = max(v, action_value)

            #Pruning
            if v == 1: break
    
        return actions_values[v]

    # O aims to minimize the score
    else:
        v = math.inf
        for action in actions(board):
            action_value = max_value(result(board,action))
            actions_values[action_value] = action
            v = min(v, action_value)
            
            #Pruning
            if v == -1: break
        
        return actions_values[v]



def max_value(board): 
    """
    Picks action a in actions(s) that produces highest value of min_value()
    """
    
    # Game over - Return the utility
    if terminal(board):
        return utility(board)

    # Finding Recursive a terminal state with all possible actions
    v = - math.inf
    
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    
    return v


def min_value(board):
    """
    Picks action a in actions(s) that produces smallest value of max_value()
    """

    # Game over - Return the utility
    if terminal(board):
        return utility(board)
    
    # Finding Recursive a terminal state with all possible actions
    v = math.inf
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    
    return v