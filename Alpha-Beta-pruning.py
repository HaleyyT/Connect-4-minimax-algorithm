import math

# constants
NUM_ROWS = 6
NUM_COLS = 7
BOTTOM_ROW = 0
LEFTMOST_COL = 0
TOP_ROW = 5
RIGHTMOST_COL = 6
BLANK = '.'
TOKEN_RED = 'r'
TOKEN_YEL = 'y'
PLAYER_RED = 'red'
PLAYER_YEL = 'yellow'


# return a list of columns (indexes) where a token can be placed
def possible_move(board): 
    column_ls = []
    # if the top cell in a column is empty, the column is available
    for col in range(NUM_COLS):
        if board[TOP_ROW][col] == BLANK:
            column_ls.append(col)
    return column_ls 


# return a new board with a new token placed
def place_token(board, col, turn):
    new_board = [row.copy() for row in board]
    token = TOKEN_RED if turn == PLAYER_RED else TOKEN_YEL
    
    # place token in the first available blank cell starting from the bottom row
    for row in range(BOTTOM_ROW, NUM_ROWS):
        if new_board[row][col] == BLANK:
            new_board[row][col] = token
            break  
    return new_board


# given function signature
def UTILITY(state):
    if is_winning(PLAYER_RED, state):
        return 10000
    elif is_winning(PLAYER_YEL, state):
        return -10000
    else:
        return 0


# check if player is winning
def is_winning(player, state):
    return (NUM_IN_A_ROW(4, state, player) > 0 or 
            NUM_IN_A_ROW(5, state, player) > 0 or 
            NUM_IN_A_ROW(6, state, player) > 0 or 
            NUM_IN_A_ROW(7, state, player) > 0)


# given function signature
def EVALUATION(state):
    return SCORE(state, PLAYER_RED) - SCORE(state, PLAYER_YEL)


# given function signature
def SCORE(state, player):
    return (count_num_tokens(state, player) +
            10 * NUM_IN_A_ROW(2, state, player) +
            100 * NUM_IN_A_ROW(3, state, player))


# return number of tokens of a player on the board (state)
def count_num_tokens(state, player):
    token = TOKEN_RED if player == PLAYER_RED else TOKEN_YEL
    count = 0
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            if state[row][col] == token:
                count += 1
    return count


# given function signature
def NUM_IN_A_ROW(count, state, player):
    token = TOKEN_RED if player == PLAYER_RED else TOKEN_YEL
    total = 0        

    # count left -> right
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - count + 1):
            matching = True
            for add in range(count):
                if state[row][col + add] != token:
                    matching = False
                    break
            if matching and (col + count > RIGHTMOST_COL or state[row][col + count] != token):
                total += 1

    # count bottom -> top
    for row in range(NUM_ROWS - count + 1):
        for col in range(NUM_COLS):
            matching = True
            for add in range(count):
                if state[row + add][col] != token:
                    matching = False
                    break
            if matching and (row + count > TOP_ROW or state[row + count][col] != token):
                total += 1

    # count bottom-left -> top-right
    for row in range(NUM_ROWS - count + 1):
        for col in range(NUM_COLS - count + 1):
            matching = True
            for add in range(count):
                if state[row + add][col + add] != token:
                    matching = False
                    break
            if matching and ((row + count > TOP_ROW) or (col + count > RIGHTMOST_COL) or 
                             state[row + count][col + count] != token):
                total += 1

    # count top-left -> bottom-right
    for row in range(count - 1, NUM_ROWS):
        for col in range(NUM_COLS - count + 1):
            matching = True
            for dif in range(count):
                if state[row - dif][col + dif] != token:
                    matching = False
                    break
            if matching and ((row - count < BOTTOM_ROW) or (col + count > RIGHTMOST_COL) or 
                             state[row - count][col + count] != token):
                total += 1

    return total


# task 1 function
# return a 2-line string (column index, # of nodes examined)
def connect_four_ab(contents, turn, max_depth):
    global num_examined_node  
    num_examined_node = 0

    # Convert board string to list of lists
    board = [list(row) for row in contents.split(',')]
    col_next_move = minimax(board, turn, max_depth, -math.inf, math.inf)[0]

    return str(col_next_move) + "\n" + str(num_examined_node)


# recursive helper function for connect_four_mm
# return a tuple of best next move (column index, max/min value)
# column index = -1 if terminal node
def minimax(board, turn, depth, alpha, beta):
    global num_examined_node
    num_examined_node += 1

    # list of column indexes
    possible_moves = possible_move(board)
    col_best_node = -1

    # base cases - terminal nodes
    util = UTILITY(board)
    if util != 0:  # someone is winning
        return col_best_node, util 

    if depth == 0:  # reached the max depth
        return col_best_node, EVALUATION(board)

    if not possible_moves:  # board full of tokens
        return col_best_node, EVALUATION(board)

    if turn == PLAYER_RED:
        max_val = -math.inf
        for col in possible_moves:
            new_board = place_token(board, col, turn)
            # value of evaluation
            value = minimax(new_board, PLAYER_YEL, depth - 1, alpha, beta)[1] 
            if value > max_val:
                max_val = value
                col_best_node = col 
            alpha = max(value, alpha)
            # pruning
            if beta <= alpha: 
                break
        return col_best_node, max_val

    # yellow
    else:
        min_val = math.inf 
        for col in possible_moves:
            new_board = place_token(board, col, turn)
            # value of evaluation
            value = minimax(new_board, PLAYER_RED, depth - 1, alpha, beta)[1] 
            if value < min_val:
                min_val = value
                col_best_node = col
            beta = min(beta, value)
            # pruning
            if beta <= alpha:
                break
        return col_best_node, min_val


if __name__ == '__main__':
    observed = connect_four_ab(".......,.......,.......,.......,.......,.......", "red", 1)
    print(observed)