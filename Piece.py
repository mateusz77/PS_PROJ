import pygame
import os


b_bishop = pygame.image.load(os.path.join("img","black_bishop.png"))
b_king = pygame.image.load(os.path.join("img","black_king.png"))
b_knight = pygame.image.load(os.path.join("img","black_knight.png"))
b_rook= pygame.image.load(os.path.join("img","black_rook.png"))
b_pawn = pygame.image.load(os.path.join("img","black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img","black_queen.png"))

w_bishop = pygame.image.load(os.path.join("img","white_bishop.png"))
w_king = pygame.image.load(os.path.join("img","white_king.png"))
w_knight = pygame.image.load(os.path.join("img","white_knight.png"))
w_rook= pygame.image.load(os.path.join("img","white_rook.png"))
w_pawn = pygame.image.load(os.path.join("img","white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img","white_queen.png"))

b = [b_bishop,b_king,b_knight,b_pawn,b_queen,b_rook]
w = [w_bishop,w_king,w_knight,w_pawn,w_queen,w_rook]

B = []
W = []

for img in b:
    B.append(pygame.transform.scale(img , (55,55)))
for img in w:
    W.append(pygame.transform.scale(img , (55,55)))


class Piece:
    img = -1 # never use that class (act like abstract)
    rect = (113,113,525,525)
    startX = rect[0]
    startY = rect[1]
    def __init__(self , row , col ,color): # make it shows all the possible moves for that piece
        self.row = row
        self.col = col
        self.color = color
        self.selected = False

    def isSelected(self):
        return self.selected

    def draw(self , win ,board):
        # different form of movement so draw would be separated
        if self.color == "w":
            drawThis = W[self.img]  # choose proper idex of list which relate to self index of image
        else:
            drawThis = B[self.img]

        if self.selected:
            moves = self.valid_moves(board)

            for move in moves:
                x = 33 + round(self.startX + (move[0] * self.rect[2] / 8))
                y = 33 + round(self.startY + (move[1] * self.rect[3] / 8))  # add five to center the position
                pygame.draw.circle(win, (255,0,0),(x,y),10)

        x = 5 + round(self.startX + (self.col * self.rect[2]/8))
        y = 5 + round(self.startY + (self.row * self.rect[3]/8)) # add five to center the position

        win.blit(drawThis, (x, y))
        if self.selected:

            pygame.draw.rect(win,(255,0,0),(x,y,55,55),2)





class Bishop(Piece):
    img = 0
    def valid_moves(self,board):
        i = self.row
        j = self.col
        return []


class Rook(Piece):
    img = 5
    def valid_moves(self,board):

        i = self.row
        j = self.col
        moves = []
        # UP
        for x in range(i-1,-1,-1):
            p = board[x][j]
            if p == 0:
                moves.append((j,x))
            else:
                break

        # DOWN
        for x in range(i+1,8,1):
            p = board[x][j]
            if p == 0:
                moves.append((j,x))
            else:
                break

        # LEFT

        for x in range(j-1,-1,-1):
            p = board[i][x]
            if p == 0:
                moves.append((x,i))
            else:
                break
        # RIGHT
        for x in range(j+1,8,1):
            p = board[i][x]
            if p == 0:
                moves.append((x,i))
            else:
                break
        return moves



class King(Piece):
    img = 1
    def valid_moves(self,board):
        i = self.row
        j = self.col
        moves = []
        # DOWN LEFT
        if i < 7:
            if j > 0: # top left
                p = board[i+1][j-1]
                if p == 0:
                    moves.append((j - 1, i + 1))
                elif p.color != self.color:
                    moves.append((j - 1, i + 1))
        # DOWN MIDDLE
        if i < 7:
            p = board[i + 1][j]
            if p == 0 :
                moves.append((j, i + 1))
            elif p.color != self.color:
                moves.append((j, i + 1))
        # DOWN RIGHT
        if i < 7:
            if j < 7: # top left
                p = board[i+1][j+1]
                if p == 0:
                    moves.append((j + 1, i + 1))
                elif p.color != self.color:
                    moves.append((j + 1, i + 1))
        # UP LEFT
        if i > 0:
            if j > 0: # top left
                p = board[i-1][j-1]
                if p == 0:
                    moves.append((j - 1, i - 1))
                elif p.color != self.color:
                    moves.append((j - 1, i - 1))
        # UP MIDDLE
        if i < 0:
            p = board[i + 1][j]
            if p == 0 :
                moves.append((j, i - 1))
            elif p.color != self.color:
                moves.append((j, i - 1))
        # UP RIGHT
        if i  < 0:
            if j < 7: # top left
                p = board[i+1][j+1]
                if p == 0:
                    moves.append((j + 1, i + 1))
                elif p.color != self.color:
                    moves.append((j + 1, i + 1))
        # left middle
        if j > 0:
            p = board[i][j-1]
            if p == 0:
                moves.append((j - 1, i))
            elif p.color != self.color:
                moves.append((j - 1, i))
        if j < 7:
            p = board[i][j+1]
            if p == 0 :
                moves.append((j + 1, i))
            elif p.color != self.color:
                moves.append((j + 1, i))
        # right middle
        return moves

class Queen(Piece):
    img = 4
    def valid_moves(self , board):

        '''
        i = self.row
        j = self.col

        moves = []

        #  UP RIGHT DIAGONAL
        curCol = j
        for row in range(0,8):
            if curCol - 1 >= 0:
                m1 = board[row][curCol-1]
            if curCol + 1 <= 7:
                m2 = board[row][curCol+1]

            curCol += 1
        '''
        return []
class Knight(Piece):
    img = 2
    def valid_moves(self,board):
        i = self.row
        j = self.col
        moves = []
        # DOWN LEFT
        if i < 6 and j > 0:
            p = board[i + 2][j-1]
            if p == 0:
                moves.append((j-1, i + 2))
            elif p.color != self.color:
                moves.append((j - 1, i + 2))

        # DOWN RIGHT
        if i < 6 and j < 7:
            p = board[i + 2][j + 1]
            if p == 0:
                moves.append((j + 1, i + 2))
            elif p.color != self.color:
                moves.append((j + 1, i + 2))
        # LEFT DOWN
        if i < 7 and j > 1:
            p = board[i + 1][j - 2]
            if p == 0:
                moves.append((j - 2, i + 1))
            elif p.color != self.color:
                moves.append((j - 2, i + 1))
        # RIGHT DOWN
        if i < 7 and j < 6:
            p = board[i + 1][j + 2]
            if p == 0:
                moves.append((j + 2, i + 1))
        # UP LEFT
        if i > 1 and j > 0:
            p = board[i - 2][j-1]
            if p == 0:
                moves.append((j-1  , i - 2))
            elif p.color != self.color:
                moves.append((j - 1, i - 2))

        # UP RIGHT
        if i > 1 and j < 7:
            p = board[i  - 2 ][j + 1]
            if p == 0:
                moves.append((j + 1, i - 2))
            elif p.color != self.color:
                moves.append((j + 1, i - 2))
        # LEFT UP
        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            if p == 0:
                moves.append((j - 2, i - 1))
            elif p.color != self.color:
                moves.append((j - 2, i - 1))
        # RIGHT UP
        if i > 0 and j < 6:
            p = board[i - 1][j + 2]
            if p == 0:
                moves.append((j + 2, i - 1))
            elif p.color != self.color:
                moves.append((j + 2, i - 1))
        return moves

class Pawn(Piece):
    img = 3
    def valid_moves(self,board):
        i = self.row
        j = self.col
        moves = []
        if self.color == "b":
            print(board[1][1])
            print(board[2][1])
            print(board[2][2])
            print(board[3][2])
            print(board[6][1])

            if self.first:
                if i < 6 :
                    p = board[i+2][j]
                    p2 = board[i+1][j]
                    if p == 0 and p2 == 0:
                        moves.append((j,i+2))
                    elif p.color != self.color:
                        moves.append((j, i + 2))
            if i < 7:
                p = board[i + 1][j]
                if p == 0 :
                    moves.append((j, i + 1))
                elif p.color != self.color:
                    moves.append((j, i + 1))

                #DIAGONAL

                if j < 7:
                    p = board[i+1][j+1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((j+1,i+1))
                if j > 0:
                    print("xd")
                    p = board[i+1][j-1]
                    print(str(p))
                    if p != 0:
                        print("xd2")
                        print(str(p))
                        if p.color != self.color:
                            print("xd3")
                            moves.append((j-1,i+1))
        else:
            if self.first:
                if i > 1 :
                    p = board[i-2][j]
                    p2 = board[i-1][j]
                    if p == 0 and p2 == 0:
                        moves.append((j,i-2))
                    elif p.color != self.color:
                        moves.append((j, i - 2))
            if i > 0:
                p = board[i - 1][j]
                if p == 0 :
                    moves.append((j, i - 1))
                elif p.color != self.color:
                    moves.append((j, i - 1))
                #DIAGONAL

                if j < 7:
                    p = board[i-1][j+1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((j+1,i-1))
                if j > 0:
                    p = board[i-1][j-1]
                    if p != 0:
                        if p.color != self.color:
                            moves.append((j-1,i-1))

        return moves
    def __init__(self ,row , col ,color):
        super().__init__(row,col,color)
        self.first = True
        self.queen = False # it can become queen


