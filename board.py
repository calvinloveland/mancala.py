import copy

class board:

    mancala = [0, 0]
    marbles = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
    player2_turn = False
    game_over = False

    def __init__(self, board=None, move=None):
        if board is not None:
            self.mancala = copy.deepcopy(board.mancala)
            self.marbles = copy.deepcopy(board.marbles)
            self.player2_turn = copy.deepcopy(board.player2_turn)
            self.game_over = copy.deepcopy(board.game_over)
            if move is not None:
                self.execute_turn(move)

    def execute_turn(self, n):
        current_player = self.player2_turn
        j = n
        moving_marbles = self.marbles[int(self.player2_turn)][n]
        switch_turns = True
        self.marbles[int(self.player2_turn)][n] = 0
        if moving_marbles == 0:
            self.game_over = True
            self.mancala[int(self.player2_turn)] = -1
        for i in range(moving_marbles):
            if j + 1 > 5 and current_player == self.player2_turn:
                j = -1
                self.mancala[int(current_player)] += 1
                if i != moving_marbles - 1:
                    current_player = not current_player
                else:
                    switch_turns = False
            else:
                if current_player != self.player2_turn:
                    j = -1
                    current_player = not current_player
                j += 1
                self.marbles[int(current_player)][j] += 1
                if self.marbles[int(current_player)][j] == 1 and current_player == self.player2_turn and i == moving_marbles - 1:
                    self.mancala[int(current_player)] += self.marbles[int(not current_player)][5-j] +1
                    self.marbles[int(not current_player)][5-j] = 0
                    self.marbles[int(current_player)][j] = 0
        if sum(self.marbles[0]) == 0:
            self.game_over = True
            self.mancala[1] += sum(self.marbles[1])
        elif sum(self.marbles[1]) == 0:
            self.game_over = True
            self.mancala[0] += sum(self.marbles[0])
        if switch_turns:
            self.player2_turn = not self.player2_turn

    def print_board(self):
        print(str(int(self.player2_turn)+1))
        print(str(self.mancala[0]) + '<-' + str(list(reversed(self.marbles[0]))) + '<-')
        print(' ->' +str(self.marbles[1]) + '->' + str(self.mancala[1]))
        if self.game_over:
            print('GAME OVER')
            print('PLAYER ' + str(int(self.mancala[0] < self.mancala[1])+1) + ' WINS')

    def get_current_player_score(self):
        return self.mancala[int(self.player2_turn)]
