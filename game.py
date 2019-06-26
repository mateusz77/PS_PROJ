import pygame
import os
import math
import time
from Board import Board

pygame.font.init()
board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")),(750,750))

# double scale
rect = (113,113,525,525)

def redraw_gameWindow(win , bo , p1time , p2time):

    win.blit(board,(0,0)) # this allow imaget to be part of a game screen
    bo.draw(win)
    formatTime1 = str(int(p1time//60)) + ":" +str(int(p1time%60))
    formatTime2 = str(int(p2time//60)) + ":" +str(int(p2time%60))
    font = pygame.font.SysFont("comicsans", 30)
    txt = font.render("Player 1 time: " + formatTime1, 1, (255, 255, 255))
    txt2 = font.render("Player 2 time: " + formatTime2, 1, (255, 255, 255))
    win.blit(txt, (550,10))
    win.blit(txt2, (550,700))

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
    return -1,-1

def end_screen(win , text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans" , 80)
    txt = font.render(text,1,(255,0,0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT+1, 3000) # if end sset time to 3 seconds

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run =  False
            elif event.type == pygame.USEREVENT + 1:
                run = False

def main():


    p1Time = 60 * 5
    p2Time = 60 * 5
    turn = "w"
    bo = Board(8, 8)
    clock = pygame.time.Clock()
    run = True
    startTime = time.time()
    while run:
        clock.tick(10)
        timeGone = int(time.time())
        if turn == "w":

            p1Time = 300 - (time.time() - startTime) # current time - beggining time
            if p1Time <= 0:
                end_screen(win,"Black Win")

        else:

            p2Time = 300  - (time.time() - startTime)
            if p2Time <= 0:
                end_screen(win,"White Win")


        redraw_gameWindow(win , bo ,p1Time,p2Time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit() # quit app at all
                pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                bo.update_moves()
                i , j = click(pos)


                change = bo.select(j,i , turn)
                if change:
                    #timeGone = int(time.time() - startTime)
                    startTime = time.time() # if made move reset time
                    if turn == "w":
                        turn = "b"
                    else:
                        turn = "w"






width = 750
height = 750

win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Chess Game")
main()
