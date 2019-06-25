import Piece
import os
import pygame



class Board:

    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols

        self.board = [[0 for x in range(8)] for _ in range(rows)]

        self.board[0][0] = Piece.Rook(0,0,"b")
        self.board[0][1] = Piece.Knight(0,1,"b")
        self.board[0][2] = Piece.Bishop(0,2,"b")
        self.board[0][3] = Piece.Queen(0,3,"b")
        self.board[0][4] = Piece.King(0,4,"b")
        self.board[0][5] = Piece.Bishop(0,5,"b")
        self.board[0][6] = Piece.Knight(0,6,"b")
        self.board[0][7] = Piece.Rook(0,7,"b")

        '''self.board[1][0] = Piece.Pawn(1, 0, "b")
        self.board[1][1] = Piece.Pawn(1, 1, "b")
        self.board[1][2] = Piece.Pawn(1, 2, "b")
        self.board[1][3] = Piece.Pawn(1, 3, "b")
        self.board[1][4] = Piece.Pawn(1, 4, "b")
        self.board[1][5] = Piece.Pawn(1, 5, "b")
        self.board[1][6] = Piece.Pawn(1, 6, "b")
        self.board[1][7] = Piece.Pawn(1, 7, "b")'''

        self.board[7][0] = Piece.Rook(7, 0, "w")
        self.board[7][1] = Piece.Knight(7, 1, "w")
        self.board[7][2] = Piece.Bishop(7, 2, "w")
        self.board[7][3] = Piece.Queen(7, 3, "w")
        self.board[7][4] = Piece.King(7, 4, "w")
        self.board[7][5] = Piece.Bishop(7, 5, "w")
        self.board[7][6] = Piece.Knight(7, 6, "w")
        self.board[7][7] = Piece.Rook(7, 7, "w")

        '''self.board[6][0] = Piece.Pawn(6,0,"w")
        self.board[6][1] = Piece.Pawn(6,1,"w")
        self.board[6][2] = Piece.Pawn(6,2,"w")
        self.board[6][3] = Piece.Pawn(6,3,"w")
        self.board[6][4] = Piece.Pawn(6,4,"w")
        self.board[6][5] = Piece.Pawn(6,5,"w")
        self.board[6][6] = Piece.Pawn(6,6,"w")
        self.board[6][7] = Piece.Pawn(6,7,"w")'''

        #self.board[3][7] = Piece.Pawn(3, 7, "w")

    def draw(self,win,board):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win,board)
    def select(self,i,j):

        act_i = i;
        act_j = j;
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False
        if self.board[i][j] != 0:
            self.board[act_i][act_j].selected = True
    def move(self,start,end):
        removed = self.board[end[1]][end[0]]
        self.board[end[1]][end[0]] = self.board[start[1]][start[0]]
        self.board[start[1]][start[0]] = 0
        return removed
if __name__ == '__main__':
    pass
