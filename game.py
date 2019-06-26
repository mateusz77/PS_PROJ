import pygame
import os
import sys
import math
import time
import socket
import pickle
import struct
from Board import Board
from config import *

# Network Site

host = SERVER_ADDRESS
port = SERVER_PORT

buffer_size = BUFFER_SIZE

servers = []
message = None
tcpClientA = None


def find_servers():
    message = "Looking for servers"
    encoded_message = message.encode()
    mcast_grp = (MCAST_GROUP, SERVER_PORT)
    client_mcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_mcast.settimeout(1)
    ttl = struct.pack('b',1)
    client_mcast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        sent = client_mcast.sendto(encoded_message, mcast_grp)
        while True:
            data, addr = client_mcast.recvfrom(1024)
            print(f"Chess server {addr[0]} available.")
            servers.append(addr[0])
    except:
        client_mcast.close()
    finally:
        client_mcast.close()


####################### INITIAL CONNECTION ###########################

find_servers()
if (len(servers) > 0):
    host = servers[0]
    port = SERVER_PORT
    tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpClientA.connect((host, port))


    my_idx = 0
    my_idx = pickle.dumps(my_idx)
    tcpClientA.send(my_idx)


    message = tcpClientA.recv(BUFFER_SIZE)
    message = pickle.loads(message)

if message == "white" or message == "black":

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

    def main(tcpClient, message):

        color = message

        p1Time = 60 * 5
        p2Time = 60 * 5
        turn = "w"
        bo = Board(8, 8)
        clock = pygame.time.Clock()
        run = True
        myTurn = False
        startTime = time.time()

        if message == "white":
            myTurn = True
            turn = "w"
        else:
            myTurn = False
            turn = "b"

        while run:

            clock.tick(10)
            timeGone = int(time.time())
            if turn == "w":
                if myTurn:
                    p1Time = 300 - (time.time() - startTime) # current time - beggining time
                else:
                    p1Time = 300
                if p1Time <= 0:
                    data = "WIN"
                    data = pickle.dumps(data)
                    tcpClient.send(data)
                    end_screen(win,"Black Win")

            else:

                if myTurn:
                    p2Time = 300  - (time.time() - startTime)
                else:
                    p2Time = 300
                if p2Time <= 0:
                    data = "WIN"
                    data = pickle.dumps(data)
                    tcpClient.send(data)
                    end_screen(win,"White Win")


            redraw_gameWindow(win , bo ,p1Time,p2Time)


            if myTurn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        data = "EXIT"
                        data = pickle.dumps(data)
                        tcpClient.send(data)
                        tcpClient.close()
                        quit() # quit app at all
                        pygame.quit()

                    if event.type == pygame.MOUSEMOTION:
                        pass
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        bo.update_moves()
                        i , j = click(pos)


                        change, prev = bo.select(j,i , turn)
                        if change:
                            #timeGone = int(time.time() - startTime)
                            curr = (i,j)
                            data_send = (prev, curr, color)
                            data_send = pickle.dumps(data_send)
                            tcpClient.send(data_send)
                            startTime = time.time() # if made move reset time
                            if turn == "w":
                                turn = "b"
                            else:
                                turn = "w"
                            myTurn = False

            else:
                data, address = tcpClient.recv(BUFFER_SIZE)

                data = pickle.loads(data)

                if isinstance(data,str):
                    if data == "WIN":
                        if color == "white":
                            end_screen(win, "White WIN")
                        else:
                            end_screen(win, "Black WIN")
                        time.sleep(5)
                        tcpClient.close()
                        sys.exit(0)
                    if data == "EXIT":
                        quit()
                        tcpClient.close()
                        pygame.quit()

                prev, curr, color = data
                change, _ = bo.select(prev[1], prev[0], turn)
                change, _ = bo.select(curr[1], curr[0], turn)
                if change:
                    # timeGone = int(time.time() - startTime)
                    startTime = time.time()  # if made move reset time
                    if turn == "w":
                        turn = "b"
                    else:
                        turn = "w"
                    myTurn = True




    width = 750
    height = 750

    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Chess Game")
    main(tcpClientA, message)