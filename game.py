import pygame
import os
import math
from Board import Board


board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")),(750,750))

# double scale
rect = (113,113,525,525)

def redraw_gameWindow():
    global  win

    win.blit(board,(0,0)) # this allow imaget to be part of a game screen

    bo.draw(win ,bo.board)
    #pygame.draw.rect(win , (255,0,0) , (113,113,525,525) , 5) # used to draw pieces
    pygame.display.update() # casual game update

def click(pos):
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]: # check mouse positon
            divX = x - rect[0]
            divY = y - rect[1]
            i = math.floor(divX / ((rect[2])/8))
            j = math.floor (divY / ((rect[2])/8))
            return i , j



def main():
    global bo
    bo = Board(8, 8)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(10)
        redraw_gameWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit() # quit app at all
                pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                i , j = click(pos)
                if bo.board[j][i] != 0:
                    bo.select(j,i)


width = 750
height = 750

win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Chess Game")
main()
