# imports the random module for randomization, Python Chess library for playing and analysing chess games and minimax library
import chess as chess
import chess.engine
from main import minimax
import random

# define the constants
MAX_DEPTH = 3
WIN_SCORE = 1000

# create the chess board and engine
board = chess.Board()

# this function applies the minimax algorithm with alpha-beta pruning
def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    if maximizing_player:
        max_eval = -float('inf')
        best_move = None

        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)[0]
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None

        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)[0]
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval, best_move


# this method examines a given chessboard position and provides a score that shows how much the white player is likely to win
# the following input is required:
# board: the evaluation position on the chess board
# if black is winning, a negative score is returned; if white is winning, a positive score is returned
# score of 0 denotes an even or deadlocked situation
def evaluate_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -WIN_SCORE
        else:
            return WIN_SCORE
    elif board.is_stalemate():
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue

        if piece.color == chess.WHITE:
            score += piece_value(piece)
        else:
            score -= piece_value(piece)

    return score


# the value of a particular chess piece is returned by this function based on its type
# the following input is required:
# piece: the evaluation chess piece
# with pawns having the lowest value (1) and queens having the highest, it produces a score representing the relative strength of the piece (9)
# piece type that is invalid yields a value of 0
def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    else:
        return 0

# the human player is prompted to enter a move in UCI notation and the move is then applied to the global chess board object by this function
# if the move entered is legitimate, it verifies that it is applied to the board and prints the move that was really played
def human_move():
    while True:
        try:
            move = input("Your move: ")
            move = chess.Move.from_uci(move)
            if move in board.legal_moves:
                board.push(move)
                print("You played:", move)
                break
            else:
                print("Invalid move. Please try again.")
        except:
            print("Invalid input. Please try again.")


# define the function to make a move for the computer player
def computer_move():
    depth = 3
    best_move = chess.Move.null()
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        score = minimax(depth - 1, alpha, beta, False)
        board.pop()
        if score > alpha:
            alpha = score
            best_move = move
    board.push(best_move)
    print("Computer played:", best_move)


# this function is checking if the game is over
def game_over():
    return board.is_game_over()


# this function is checking if the game is a draw
def is_draw():
    return board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves()

# this function is checking if it is a checkmate
def is_checkmate():
    return board.is_checkmate()


# it is the main function which is used to run the game
def play_game():
    print("Welcome to Chess!")
    print(board)

    while not game_over():
        human_move()
        print(board)

        if is_checkmate():
            print("Checkmate! You win!")
            return

        if is_draw():
            print("Draw!")
            return

        computer_move()
        print(board)

        if is_checkmate():
            print("Checkmate! Computer wins!")
            return

        if is_draw():
            print("Draw!")
            return


# start the game
board = chess.Board()
play_game()