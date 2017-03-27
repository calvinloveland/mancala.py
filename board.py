class board:
    mancala = [0,0]
    marbles = [[4,4,4,4,4,4],[4,4,4,4,4,4]]
    player2_turn = False
    game_over = False

    def execute_turn(self,n):
        current_player = self.player2_turn
        j = n
        moving_marbles = self.marbles[int(self.player2_turn)][n]
        switch_turns = True
        self.marbles[int(self.player2_turn)][n] = 0
        for i in range(moving_marbles):
            if j+1 > 5:
                j = -1
                if current_player == self.player2_turn:
                    self.mancala[int(current_player)] += 1
                if i != moving_marbles-1:
                    current_player = not current_player
                else:
                    switch_turns = False
            else:
                j += 1
                self.marbles[int(current_player)][j] += 1
                if self.marbles[int(current_player)][j] == 1 and current_player == self.player2_turn and i == moving_marbles-1:
                    self.mancala[int(current_player)] += self.marbles[int(not current_player)][j]
                    self.marbles[int(not current_player)][j] = 0
        if sum(self.marbles[0]) == 0 or sum(self.marbles[1]) == 0:
            self.game_over = True
        if switch_turns:
            self.player2_turn = not self.player2_turn
        if self.game_over:
            print('GAME OVER')
            print('PLAYER ' + str(int(self.mancala[0] < self.mancala[1])) + ' WINS')

    def print_board(self):
        print(int(self.player2_turn))
        for j in range(2):
            print(self.mancala[j])
            print(self.marbles[j])
