import board
import random


def alpha_beta(board_arg, depth, alpha, beta, player):
    if depth == 0 or board_arg.game_over:
        if board_arg.game_over:
            if board_arg.mancala[int(player)] > board_arg.mancala[int(not player)]:
                return [500, -1]
            return [-500, -1]
        return [(board_arg.mancala[int(player)] - board_arg.mancala[int(not player)]) + (sum(board_arg.marbles[int(player)]) - sum(board_arg.marbles[int(not player)])), -1]
    if player == board_arg.player2_turn:
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
            #if depth == 4:
                #new_board.print_board()
        return v
    else:
        v = [10000, -1]
        for i in range(6):
            new_board = board.board(board_arg, i)
            v[0] = min(v[0], alpha_beta(new_board, depth - 1, alpha, beta, player)[0])
            beta = min(beta, v[0])
            if beta <= alpha:
                break
            #if depth == 3:
                #new_board.print_board()
        return v

'''
testing_board = board.board()
testing_board.mancala = [3,5]
testing_board.marbles = [[3,9,10,11,2,3],[0,0,0,0,0,1]]
alpha_beta(testing_board,4,-1000,1000,False)
print("DING")
input()
'''

clean_board = board.board()
wins = [0,0]
for i in range(100):
    current_board = board.board(clean_board)
    print("NEW GAME")
    current_board.print_board()

    while not current_board.game_over:
        if not current_board.player2_turn:
            ab_result = alpha_beta(current_board, 9, -1000, 1000, False)
            print(ab_result)
            current_board.execute_turn(ab_result[1])
        else:
            move = (int(input('Your move madam?:'))-1)
            while current_board.marbles[1][move] == 0:
                  move = (int(input('Your move madam?:'))-1)
            current_board.execute_turn(move)
        current_board.print_board()
    if current_board.mancala[0] < current_board.mancala[1]:
        input()
    wins[int(current_board.mancala[0] > current_board.mancala[1])] += 1
print(wins)
