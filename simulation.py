from math import inf
import sys
import os
import time
import random

PLAYERS = ['IA_random', 'IA_minimax', 'IA_minimax_AB']
PLAYER1 = -1
PLAYER2 = 1
VOID = 0
LEGEND = dict(zip((VOID, PLAYER1, PLAYER2), (" ", "O", "X")))

def evaluate(board):
    """
    Perform heuristic evaluation from board.
    Heuristic - allow the computer to discover the solution
    of some problems by itself.
    """
    if wins(board, PLAYER2):
        return PLAYER2
    if wins(board, PLAYER1):
        return PLAYER1
    return VOID

def empty_cells(board):
    """Extract the remainder of board"""
    cells = []  # it contains all empty cells
    # Use enumerate for easy indexing
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == VOID:
                cells.append((i, j))
    return cells

# Row calc example to split wins code
def win_row(board, player, nb_win_case):
    for row in board:
        isRow = 0
        for col in row:
            if col == player:
                isRow += 1
                if isRow == nb_win_case:
                    return True
            # Reset isRow on Void cases
            elif isRow:
                isRow = 0
    return False

# Col calc example to split wins code
def win_col(board, player, nb_win_case):
    isCol = [0 for _ in range(0, len(board))]
    for row in board:
        for y, col in enumerate(row):
            if col == player:
                isCol[y] += 1
                if isCol[y] == nb_win_case:
                    return True
            # Reset isCol[col] on Void cases
            elif isCol[y]:
                isCol[y] = 0
    return False

# Diag calc example to split wins code
def win_diag(board, player, nb_win_case):
    for x, row in enumerate(board):
        if x + nb_win_case > len(board):
            break
        for y, col in enumerate(row):
            # Cherche dans y meme si y + nb_win_case > len(board) car il cherche dans diagonal gauche et droite en un seul for
            if col == player:
                isDiagL = 0
                isDiagR = 0
                for i in range(0, nb_win_case):
                    if y + i < len(board) and board[x+i][y+i] == player:
                        isDiagL += 1
                    if y >= i and board[x+i][y-i] == player:
                        isDiagR += 1
                if isDiagL == nb_win_case or isDiagR == nb_win_case:
                    return True

def wins(board, player, nb_win_case: int = 4):
    if nb_win_case > len(board):
        nb_win_case = len(board)
    # version splitté en plusieurs fonction mais moins optimisé
    # return win_row(board, player, nb_win_case) \
    #     or win_col(board, player, nb_win_case) \
    #     or win_diag(board, player, nb_win_case)
    isCol = []
    for x, row in enumerate(board):
        isRow = 0
        for y, col in enumerate(row):
            # Init cols on first row
            if x == 0:
                isCol.append(0)
            if col == player:
                # Check row
                isRow += 1
                if isRow == nb_win_case:
                    return True
                # Check cols
                isCol[y] += 1
                if isCol[y] == nb_win_case:
                    return True
                # Check digonals
                if x + nb_win_case <= len(board):
                    isDiagL = 0
                    isDiagR = 0
                    for i in range(0, nb_win_case):
                        if y + i < len(board) and board[x+i][y+i] == player:
                            isDiagL += 1
                        if y >= i and board[x+i][y-i] == player:
                            isDiagR += 1
                    if isDiagL == nb_win_case or isDiagR == nb_win_case:
                        return True
            else:
                isRow = 0
                isCol[y] = 0
    return False

def game_over(board):
    """Check game over condition"""
    return wins(board, PLAYER1) or wins(board, PLAYER2)

def clean():
    """Clear system terminal"""
    os_name = sys.platform.lower()
    if 'win' in os_name and os_name != 'darwin':
        os.system('cls')
    else:
        os.system('clear')

def minimax(board, depth, player, true_player):
    # inf/-inf are the initial score for the players
    best = [None, None, inf if player == true_player else -inf]
    if depth == 0 or game_over(board):
        return [None, None, evaluate(board)]
        # return [None, None, evaluate(board) * ( 1 / depth if depth else 1)]
    for cell in empty_cells(board):
        # Fill the empty cells with the player symbols
        x, y = cell[0], cell[1]
        board[x][y] = player
        if evaluate(board) == true_player:
            best = [ x, y, true_player]
            board[x][y] = 0
            break
        score = minimax(board, depth - 1, -player, true_player)
        board[x][y] = 0
        score[0], score[1] = x, y
        if player == true_player:
            if score[2] < best[2]:
                best = score
        elif score[2] > best[2]:
            best = score
    return best

def minimaxWithAB(board, depth, player, true_player, alpha = -inf, beta = inf):
    # inf/-inf are the initial score for the players
    best = [None, None, inf if player == true_player else -inf]
    if depth == 0 or game_over(board):
        return [None, None, evaluate(board)]
        # return [None, None, evaluate(board) * ( 1 / depth if depth else 1)]
    for cell in empty_cells(board):
        # Fill the empty cells with the player symbols
        x, y = cell[0], cell[1]
        board[x][y] = player
        if evaluate(board) == true_player:
            best = [x, y, true_player]
            board[x][y] = 0
            break
        score = minimaxWithAB(board, depth - 1, -player, true_player, alpha, beta)
        board[x][y] = 0
        score[0], score[1] = x, y
        if player == true_player:
            if score[2] < best[2]:
                best = score
            if best[2] <= alpha:
                return best
            if best[2] < beta:
                beta = best[2]
        else:
            if score[2] > best[2]:
                best = score
            if best[2] >= beta:
                return best
            if best[2] > alpha:
                alpha = best[2]
    return best

# board : [
#     [0,0,0], 0 * 3 + 1 = 1
#     [0,0,0], 1 * 3 + 1 = 4
#     [0,0,0], 2 * 3 + 1 = 7
# ]
def nb_to_coord(move: int, board_length: int):
    for i in range(0, board_length):
        for j in range(0, board_length):
            if move == ((i * board_length) + j + 1):
                return i, j
    return None

def ai_turn(board, algo, player):
    depth = len(empty_cells(board))  # The remaining of empty cells

    if algo == 'IA_random':
        # Choix aleatoire parmis les remain
        remain = empty_cells(board)
        x, y = random.choice(remain)
    elif algo == 'IA_minimax':
        x, y, score = minimax(board, depth, player, player)
    elif algo == 'IA_minimax_AB':
        x, y, score = minimaxWithAB(board, depth, player, player)

    board[x][y] = player

def render(board):
    """Render the board board to stdout"""
    pretty_board = [[LEGEND[col] for col in row] for row in board]
    return ("{}\n" * len(pretty_board)).format(*pretty_board)

def make_board(nb: int = 3):
    return [[0 for j in range(0, nb)] for i in range(0, nb)]
    # return [[0]*nb]*nb // Ne marche, chaque ligne obtient la même id()

def main():
    clean()
    nb_simulations_ok = algo_player1_ok = algo_player2_ok = False

    while not algo_player1_ok:
            algo_player1 = str(input("Joueur 1 ("+'|'.join(PLAYERS)+") :"))
            if algo_player1 in PLAYERS:
                algo_player1_ok = True
            else:
                print("Joueur 1 incorrect : choisir parmi "+'|'.join(PLAYERS))

    while not algo_player2_ok:
            algo_player2 = str(input("Joueur 2 ("+'|'.join(PLAYERS)+") :"))
            if algo_player2 in PLAYERS:
                algo_player2_ok = True
            else:
                print("Joueur 2 incorrect : choisir parmi "+'|'.join(PLAYERS))

    while not nb_simulations_ok:
        try:
            nb_simulations = int(input("Nombre de simulations :"))
            nb_simulations_ok = True
        except ValueError:
            print("Nombre de simulations incorrect")

    clean()
    print(f"Début de {algo_player1} VS {algo_player2} ({nb_simulations} parties) !\n")

    win_player1 = win_player2 = draw = 0
    start_time = time.time()
    for i in range(nb_simulations):
        if i in list(range(0,nb_simulations,int(nb_simulations/10))):
            print(f"{i}/{nb_simulations}... ({time.strftime('%Hh%Mm%Ss', time.gmtime(time.time() - start_time))})")

        board = make_board()
        while not wins(board, PLAYER2) and len(empty_cells(board)) > 0:

            ai_turn(board, algo_player1, PLAYER1)
            if len(empty_cells(board)) == 0 or wins(board, PLAYER1):
                break

            ai_turn(board, algo_player2, PLAYER2)
        if wins(board, PLAYER1):
            win_player1 += 1
        elif wins(board, PLAYER2):
            win_player2 += 1
        else:
            draw +=1

    ratio_win_player1 = round((win_player1/nb_simulations)*100, 2)
    ratio_win_player2 = round((win_player2 / nb_simulations) * 100, 2)
    ratio_draw = round((draw / nb_simulations) * 100, 2)

    print(f"\nNombre de victoire {algo_player1} : {win_player1}/{nb_simulations} ({ratio_win_player1}%)")
    print(f"Nombre d'égalité  : {draw}/{nb_simulations} ({ratio_draw}%)")
    print(f"Nombre de victoire {algo_player2} : {win_player2}/{nb_simulations} ({ratio_win_player2}%)")

    print(f"\n--- Temps total : {time.strftime('%Hh%Mm%Ss', time.gmtime(time.time() - start_time))} ---")

if __name__ == '__main__':
    main()
