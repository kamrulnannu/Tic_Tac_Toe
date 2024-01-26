import random

board = []
board_dim = 3 # Same number of rows and columns
player1_marker = ''
palyer2_marker = ''
current_player = -1

'''
    NOTE:
    1. abc = () is not considered as set, but considered as tuple
    2. abc = set() is considered as set
'''
no_win_row_set = set()
no_win_col_set = set()

'''
There are two diagonals:
    diagonal# 1: when row_num == col_num
    diaginal# 2: when (row_num+col_num) == board_dim -1
'''
no_win_diagonal = set()

available_cell = set()

def initGame():
    global board_dim
    global board
    global current_player
    global player1_marker
    global player2_marker
    global no_win_diagonal
    global no_win_col_set
    global no_win_row_set
    global available_cell
    global current_player

    # Init global variable
    board = []
    board_dim = 3
    no_win_diagonal = set()
    no_win_col_set = set()
    no_win_row_set = set()
    available_cell = set()
    player1_marker = ''
    player2_marker = ''
    current_player = random.randint(0, 1) # Choose random between 0 and 1

    player1_marker, player2_marker = getPlayerMarker()

    valid = False
    while not valid:
        data = input("\nEnter board dimension which is greater than or equal to 3: ")
        if not data.isdigit():
            board_dim = -1
        else:
            board_dim = int(data)
        if board_dim < 3:
            print(f'Invalid board dimension!')
        else:
            valid = True

    col = []
    i = 1
    while i <= (board_dim * board_dim):
        col.append(i)
        available_cell.add(i)
        if (i % board_dim == 0):
            board.append(col)

            ''' NOTE: col.clear() will clear data which are appended in
            board by above statement. So col has to be cleared out as shown
            below to avoid clearing out appended list above
            '''
            col = []
        i += 1

def displayBoard():
    row = 0
    print(f'\nCurrent standing of board:\n')
    formated_tab = '|'.join('\t\t' for i in range(0, board_dim))
    line_len = 8 * (board_dim *2 -1) + board_dim
    formated_line = ''.join('-' for i in range(0, line_len))
    while row < board_dim:
        print(formated_tab)
        formated_out = '\t|\t'.join(str(item) for item in board[row])
        print('\t{}'.format(formated_out))
        print(formated_tab)
        print(formated_line) 
        row += 1

def getPlayerMarker():
    choice = ''
    while (choice != 'X' and choice != 'O'):
        choice = input("\nPlease enter board marker 'X' or 'O' for Player {}: ".format(current_player+1)).upper()
    
    if (current_player == 0):
        if (choice == 'X'): 
            return (choice, 'O')
        else:
            return (choice, 'X')
    else:
        if (choice == 'X'): 
            return ('O', choice)
        else:
            return ('X', choice)

def getPlayerChoice():
    s = '\nChoose a cell number from ' + str(available_cell) + ' for Player {}: '.format(current_player+1);
    valid = False
    while not valid:
        data  = input(s)
        if not data.isdigit():
            print(f'Choose a number!')
            continue
        else:
            choice = int(data)

        if choice in available_cell:
            valid = True
        else:
            print(f'Invalid cell selected!')
    return choice
    

def getRowNum(choice):
    return int((choice - 1)/board_dim)

def getColNum(choice):
    return ((choice - 1) % board_dim)

def getCell(choice):
    return getRowNum(choice), getColNum(choice)

def isCornerCell(row, col):
    if ((row == 0) or (row == board_dim-1)) and col in [0, borad_dim-1]:
        return True

    return False

def isDiagonalCell(row, col):
    if (row == col) or (row+col == board_dim - 1):
        return True
    return False

def markOnBoard(row, col):
    # print('row: {}, col {}'.format(row, col))
    if (current_player == 0):
        board[row][col] = player1_marker
    else:
        board[row][col] = player2_marker

def isWinner(row, col):
    global no_win_row_set
    global no_win_col_set
    global no_win_diagonal

    # Check in row for winner
    if row not in no_win_row_set:
        p1mark = [item for item in board[row] if item == player1_marker]
        p2mark = [item for item in board[row] if item == player2_marker]
        if (len(p1mark) > 0) and (len(p2mark) > 0):
            no_win_row_set.add(row)
        elif ((current_player == 0) and (len(p1mark) == board_dim)):
            return True
        elif ((current_player == 1) and (len(p2mark) == board_dim)):
            return True

    # Check in column for winner
    
    if col not in no_win_col_set:
        p1col = [player1_marker for i in range(0, board_dim) if board[i][col] == player1_marker]
        p2col = [player2_marker for i in range(0, board_dim) if board[i][col] == player2_marker]

        if (len(p1col) > 0) and (len(p2col) > 0):
            no_win_col_set.add(col)
        elif ((current_player == 0) and (len(p1col) == board_dim)):
            return True
        elif ((current_player == 1) and (len(p2col) == board_dim)):
            return True
        '''
        # OK
        marker1 = 0
        marker2 = 0
        for rw in board:
            if rw[col] == player1_marker:
                marker1 += 1
            elif rw[col] == player2_marker:
                marker2 += 1
        if marker2 > 0 and marker1 > 0:
            no_win_col_set.add(col)
        elif ((current_player == 0) and (marker1 == board_dim)):
            return True
        elif ((current_player == 1) and (marker2 == board_dim)):
            return True
        '''

    # Check in diagonal for winner
    marker1 = 0
    marker2 = 0
    if isDiagonalCell(row, col):
        digonal_num = 0
        if (row == col):
            diagonal_num = 1
            if diagonal_num not in no_win_diagonal:
                p1mark = [board[rc][rc] for rc in range(0, board_dim) if board[rc][rc] == player1_marker]
                p2mark = [board[rc][rc] for rc in range(0, board_dim) if board[rc][rc] == player2_marker]

                marker1 = len(p1mark)
                marker2 = len(p2mark)

                '''
                for rc in range(0, board_dim):
                    if board[rc][rc] == player1_marker:
                        marker1 += 1
                    elif board[rc][rc] == player2_marker:
                        marker2 += 1
                '''
                if marker1 > 0 and marker2 > 0:
                    no_win_diagonal.add(diagonal_num)
                elif (marker1 == board_dim) and (current_player == 0):
                    return True
                elif (marker2 == board_dim) and (current_player == 1):
                    return True
        else:
            diagonal_num = 2
            if diagonal_num not in no_win_diagonal:
                p1mark = [board[r][(board_dim-1) - r] for r in range(0, board_dim) if player1_marker == board[r][(board_dim-1)-r]]
                p2mark = [board[r][(board_dim-1) - r] for r in range(0, board_dim) if player2_marker == board[r][(board_dim-1)-r]]

                marker1 = len(p1mark)
                marker2 = len(p2mark)

                '''
                cl = board_dim-1
                for r in range(0, board_dim):
                    if board[r][cl] == player1_marker:
                        marker1 += 1
                    elif board[r][cl] == player2_marker:
                        marker2 += 1

                    cl = cl - 1
                '''
                if marker2 > 0 and marker1 > 0:
                    no_win_diagonal.add(diagonal_num)
                elif (current_player == 0) and (marker1 == board_dim):
                    return True
                elif (current_player == 1 ) and (marker2 == board_dim):
                    return True
    
    return False

'''
    isTie(): This function should be called after the isWinner() call
'''
def isTie():
    '''
    Opportunity to win:
        1. board_dim rows and
        2. board_dim columns and
        3. 2 diagonals
    '''
    opportunity_to_win = 2 * board_dim + 2

    no_win = len(no_win_row_set) + len (no_win_col_set) + len (no_win_diagonal)

    if (no_win == opportunity_to_win):
        return True

    return False

def getPlayerGameOnOrOff():
    choice = ''
    while choice != 'Y' and choice != 'N':
        choice = input("\nDo you want to continue another round of game 'Y' or 'N'?: ").upper()

    if choice == 'Y':
        return True
    else:
        return False

def main():
    global current_player
    global player1_marker
    global player2_marker

    print(f'\nWelcome to Tic Tac Toe ...')

    initGame()
    displayBoard()

    game_on = True
    prompt = False
    while game_on:
        cellId = getPlayerChoice()
        available_cell.remove(cellId)
        row, col = getCell(cellId)
        markOnBoard(row, col)
        displayBoard()
        if isWinner(row, col):
            print('\nPlayer {} won the game!!!\n'.format(current_player+1))
            prompt = True
        elif isTie():
            print(f'\nGame is Tie!!!\n')
            prompt = True

        if prompt == True:
            prompt = False
            game_on = getPlayerGameOnOrOff()
            if game_on:
                initGame()
                displayBoard()
            else:
                print(f'\nGOOD BYE!!!')
        else:
            current_player = (current_player + 1) % 2
            
if __name__ == '__main__':
    main()
