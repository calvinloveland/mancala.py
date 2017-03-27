import board
import random


def getBestMove(current_mancala,current_marbles,other_mancala,other_marbles):
    print("TODO")
def printNextMove(player,player1Mancala,player1Marbles,player2Mancala,player2Marbles):

def print_next_move_from_board(board):
    return printNextMove(int(board.player2_turn)+1,board.mancala[0],board.marbles[0],board.mancala[1],board.marbles[1])
current_board = board.board()
current_board.print_board()
while True:
    if current_board.player2_turn:
        current_board.execute_turn(print_next_move_from_board(current_board))
    else:
        current_board.execute_turn(int(input("Enter position to play:")))
    current_board.print_board()