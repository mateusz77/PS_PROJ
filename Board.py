import Piece
import os
import pygame
import numpy as np



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

        self.board[1][0] = Piece.Pawn(1, 0, "b")
        self.board[1][1] = Piece.Pawn(1, 1, "b")
        self.board[1][2] = Piece.Pawn(1, 2, "b")
        self.board[1][3] = Piece.Pawn(1, 3, "b")
        self.board[1][4] = Piece.Pawn(1, 4, "b")
        self.board[1][5] = Piece.Pawn(1, 5, "b")
        self.board[1][6] = Piece.Pawn(1, 6, "b")
        self.board[1][7] = Piece.Pawn(1, 7, "b")

        self.board[7][0] = Piece.Rook(7, 0, "w")
        self.board[7][1] = Piece.Knight(7, 1, "w")
        self.board[7][2] = Piece.Bishop(7, 2, "w")
        self.board[7][3] = Piece.Queen(7, 3, "w")
        self.board[7][4] = Piece.King(7, 4, "w")
        self.board[7][5] = Piece.Bishop(7, 5, "w")
        self.board[7][6] = Piece.Knight(7, 6, "w")
        self.board[7][7] = Piece.Rook(7, 7, "w")

        self.board[6][0] = Piece.Pawn(6,0,"w")
        self.board[6][1] = Piece.Pawn(6,1,"w")
        self.board[6][2] = Piece.Pawn(6,2,"w")
        self.board[6][3] = Piece.Pawn(6,3,"w")
        self.board[6][4] = Piece.Pawn(6,4,"w")
        self.board[6][5] = Piece.Pawn(6,5,"w")  
        self.board[6][6] = Piece.Pawn(6,6,"w")
        self.board[6][7] = Piece.Pawn(6,7,"w")

        #self.board[3][7] = Piece.Pawn(3, 7, "w")

    def update_moves(self ):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)

    def draw(self,win):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win)

    def get_danger_moves(self ,color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        for move in self.board[i][j].move_list:
                            danger_moves.append(move)
        return danger_moves
    '''
    def checkMate(self , color):   # if won the game
        danger_moves = self.get_danger_moves(color)
        king_moves = []
        block_moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == color:
                            if self.board[i][j].king:
                                for move in self.board[i][j].move_list:
                                    king_moves.append(move)
                            else:
                                for move in self.board[i][j].move_list:
                                    block_moves.append(move)


        if len(king_moves) == 0:
            return False
        for block in block_moves:
            dMoves = danger_moves[:]
            if block in danger_moves:
                dMoves.remove(block)

            for move in king_moves:
                if  move not in dMoves :
                    return False

        return True

        '''
    def is_checked(self,color):
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1,-1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].king and  self.board[i][j].color == color:
                        king_pos = (j, i)

        if king_pos in danger_moves:
            return True
        return False


    def select(self,row,col , color ):
        changed = False
        prev = (-1,-1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        prev = (i,j) #  set prev as current
                        #print(prev)
        # if piece
        if self.board[row][col] == 0:
                moves = self.board[prev[0]][prev[1]].move_list
                if (col , row) in moves:
                    changed = self.move(prev , (row,col),color)
                    #changed = True
                self.reset_selected()
        else:
            if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                moves = self.board[prev[0]][prev[1]].move_list
                if (col, row) in moves:

                    changed = self.move(prev, (row, col),color)
                    #changed = True

                self.reset_selected()
                if self.board[row][col].color == color:
                    self.board[row][col].selected = True


            else:
                self.reset_selected()
                if self.board[row][col].color == color:
                    self.board[row][col].selected = True
                #print(self.board[row][col])
        return changed



    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False


    def move(self,start,end,color):
        checkedBef = self.is_checked(color)
        changed = True
        nBoard = self.board[:] # backup board
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False;

        nBoard[start[0]][start[1]].change_pos((end[0],end[1 ]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard
        if color == "w":
            checkColor = "b"
        else:
            checkColor = "w"
        self.update_moves()
        if self.is_checked(color) or (checkedBef and self.is_checked(color)):
            changed = False
            nBoard = self.board[:]  # backup board
            if nBoard[end[0]][end[1]].pawn:
                nBoard[end[0]][end[1]].first = True;

            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self.board = nBoard
        self.update_moves()
        return changed

if __name__ == '__main__':
    pass
