import board
import random


def alpha_beta(board_arg, depth, alpha, beta, player):
    if depth == 0 or board_arg.game_over:
        #print("base")
        if board_arg.game_over:
            if board_arg.mancala[int(player)] > board_arg.mancala[int(not player)]:
                return [500, -1]
            return [-500, -1]
        return [board_arg.mancala[int(player)] - board_arg.mancala[int(not player)], -1]
    if player == board_arg.player2_turn:
        #print("max")
        v = [-10000, -1]
        best_score = -10000
        for i in range(6):
            new_board = board.board(board_arg,i)
            v[0] = max(v[0], alpha_beta(new_board, depth - 1, alpha, beta, player)[0])
            alpha = max(alpha, v[0])
            if v[0] > best_score:
                best_score = v[0]
                v[1] = i
                if beta <= alpha:
                    break
        return v
    else:
        #print("min")
        v = [10000, -1]
        for i in range(6):
            new_board = board.board(board_arg, i)
            v[0] = min(v[0], alpha_beta(new_board, depth - 1, alpha, beta, player)[0])
            beta = min(beta, v[0])
            if beta <= alpha:
                break
        return v


clean_board = board.board()
wins = [0,0]
for i in range(100):
    current_board = board.board(clean_board)
    print("NEW GAME")
    current_board.print_board()

    while not current_board.game_over:
        if not current_board.player2_turn:
            ab_result = alpha_beta(current_board, 6, -1000, 1000, False)
            print(ab_result)
            current_board.execute_turn(ab_result[1])
        else:
            ab_result = alpha_beta(current_board, 6, -1000, 1000, True)
            print(ab_result)
            current_board.execute_turn(random.randint(0,5))
        current_board.print_board()
    if current_board.mancala[0] < current_board.mancala[1]:
        input()
    wins[int(current_board.mancala[0] > current_board.mancala[1])] += 1
print(wins)
