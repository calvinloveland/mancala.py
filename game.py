import board
import random
from celery import Celery
import time

app = Celery("game", backend="rpc://", broker="pyamqp://guest:guest@localhost//")
app.conf.update(task_serializer="pickle", accept_content=["pickle", "json"])


def score_board(board_arg, player, depth):
    if board_arg.game_over:
        if board_arg.mancala[int(player)] > board_arg.mancala[int(not player)]:
            return 5000
        return -5000 - depth
    return (board_arg.mancala[int(player)] - board_arg.mancala[int(not player)]) + (
        sum(board_arg.marbles[int(player)]) - sum(board_arg.marbles[int(not player)])
    )


@app.task
def alpha_beta(board_arg, depth, alpha, beta, player, parallel=True):
    if depth == 0 or board_arg.game_over:
        return [score_board(board_arg, player, depth), -1]
    if player == board_arg.player2_turn:
        v = [-10000, -1]
        best_score = -10000
        if parallel:
            calls = list()
            for i in range(6):
                new_board = board.board(board_arg, i)
                calls.append(
                    alpha_beta.delay(new_board, depth - 1, alpha, beta, player, False)
                )
            for i in range(6):
                v[0] = max(v[0], calls[i].get()[0])
                if v[0] > best_score:
                    best_score = v[0]
                    v[1] = i
            return v
        else:
            for i in range(6):
                new_board = board.board(board_arg, i)
                v[0] = max(
                    v[0],
                    alpha_beta(new_board, depth - 1, alpha, beta, player, False)[0],
                )
                alpha = max(alpha, v[0])
                if v[0] > best_score:
                    best_score = v[0]
                    v[1] = i
                if beta <= alpha:
                    break
            return v
    else:
        if parallel:
            v = [10000, -1]
            calls = list()
            for i in range(6):
                new_board = board.board(board_arg, i)
                calls.append(
                    alpha_beta.delay(new_board, depth - 1, alpha, beta, player, False)
                )
            for i in range(6):
                v[0] = min(v[0], calls[i].get()[0])
            return v
        else:
            v = [10000, -1]
            for i in range(6):
                new_board = board.board(board_arg, i)
                v[0] = min(
                    v[0],
                    alpha_beta(new_board, depth - 1, alpha, beta, player, False)[0],
                )
                beta = min(beta, v[0])
                if beta <= alpha:
                    break
            return v


if __name__ == "__main__":
    clean_board = board.board()
    wins = [0, 0]
    player1_level = 0
    player2_level = 0
    while True:
        parallel_timings = list()
        serial_timings = list()
        current_board = board.board(clean_board)
        player1AI = True
        player2AI = True
        player1_level += 1
        player2_level += 1
        # print("Parallel (y/n)?")
        # if "n" in input().lower():
        #    parallel = False
        # print("Player1 (A)I or (P)layer?")
        # if "p" in input().lower():
        #    player1AI = False
        # else:
        #    print("AI level? (1-9)")
        #    player1_level = int(input())
        # print("Player2 (A)I or (P)layer?")
        # if "p" in input().lower():
        #    player2AI = False
        # else:
        #    print("AI level? (1-9)")
        #    player2_level = int(input())
        # current_board.print_board()
        while not current_board.game_over:
            if not current_board.player2_turn:
                if player1AI:
                    start = time.time()
                    best_move = alpha_beta(
                        current_board, player1_level, -1000, 1000, False, True
                    )[1]
                    end = time.time()
                    parallel_timings.append(end - start)
                    current_board.execute_turn(best_move)
                else:
                    move = int(input("Player1, your move?:")) - 1
                    current_board.execute_turn(move)
            else:
                if player2AI:
                    start = time.time()
                    best_move = alpha_beta(
                        current_board, player2_level, -1000, 1000, True, False
                    )[1]
                    end = time.time()
                    serial_timings.append(end - start)
                    current_board.execute_turn(best_move)
                else:
                    move = int(input("Player2, your move?:")) - 1
                    current_board.execute_turn(move)
            # current_board.print_board()
        print(
            "avg parallel timing - avg serial timing,"
            + str(player1_level)
            + ","
            + str(sum(parallel_timings) / len(parallel_timings))
            + ","
            + str(sum(serial_timings) / len(serial_timings))
        )
