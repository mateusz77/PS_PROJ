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
    client_mcast.settimeout(TIMEOUT)
    ttl = struct.pack('b',1)
    client_mcast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        sent = client_mcast.sendto(encoded_message, mcast_grp)
        while True:
            data, addr = client_mcast.recvfrom(1024)
            # print(f"Chess server {addr[0]} available.")
            # print("Chess server {} available.".format(addr[0]))
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
    tcpClientA.settimeout(TIMEOUT)
    tcpClientA.connect((host, port))


    my_idx = 0
    my_idx = pickle.dumps(my_idx)
    tcpClientA.send(my_idx)

    while True:
        try:
            message = None
            message = tcpClientA.recv(BUFFER_SIZE)
            if message:
                break
        except socket.timeout:
            pass

    message = pickle.loads(message)

    if message == "white" or message == "black":

        pygame.font.init()
        board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")),(750,750))

        # double scale
        rect = (113,113,525,525)

        def redraw_gameWindow(win , bo , p1time , p2time ,turn):

            win.blit(board,(0,0)) # this allow imaget to be part of a game screen
            bo.draw(win)
            formatTime1 = str(int(p1time//60)) + ":" +str(int(p1time%60))
            formatTime2 = str(int(p2time//60)) + ":" +str(int(p2time%60))
            font = pygame.font.SysFont("comicsans", 30)
            txt = font.render("Player White time: " + formatTime1, 1, (255, 255, 255))
            txt2 = font.render("Player Black time: " + formatTime2, 1, (255, 255, 255))
            win.blit(txt, (500,10))
            win.blit(txt2, (500,700))
            if turn == "b":
                font = pygame.font.SysFont("comicsans", 40)
                txt = font.render("Player Black Turn", 1, (255, 0, 0))
                win.blit(txt, (width / 2 - txt.get_width() / 2, 10))
                pygame.display.update()

            else:

                font = pygame.font.SysFont("comicsans", 40)
                txt = font.render("Player White Turn", 1, (255, 0, 0))
                win.blit(txt, (width / 2 - txt.get_width() / 2, 10))
                pygame.display.update()

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


        def menu_screen(win):
            run = True
            while run:
                win.fill((128, 128, 128))
                font = pygame.font.SysFont("comicsans", 80)
                txt = font.render("Online Chess", 1, (0, 128, 0))
                win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        run = False
                time.sleep(2)
                run = False
            main(tcpClientA, message)

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
                turn = "w"

            # print("MyTurn color: ", myTurn, turn, color)

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
                        tcpClient.close()
                        end_screen(win,"Black Win")
                        time.sleep(3)
                        quit()
                        pygame.quit()

                else:

                    if myTurn:
                        p2Time = 300  - (time.time() - startTime)
                    else:
                        p2Time = 300
                    if p2Time <= 0:
                        data = "WIN"
                        data = pickle.dumps(data)
                        tcpClient.send(data)
                        tcpClient.close()
                        end_screen(win,"White Win")
                        time.sleep(3)
                        quit()
                        pygame.quit()


                redraw_gameWindow(win , bo ,p1Time,p2Time , turn)


                if myTurn:
                    # print("Im IN!")
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
                            # print("Mouse BUTTON")
                            pos = pygame.mouse.get_pos()
                            bo.update_moves()
                            i , j = click(pos)


                            change, prev_mv ,ifwin = bo.select(j,i , turn)
                            if change:
                                if ifwin:
                                    if turn == "w":
                                        data = "WIN"
                                        data = pickle.dumps(data)
                                        tcpClient.send(data)
                                        end_screen(win, "White Win")
                                        time.sleep(3)
                                        tcpClient.close()
                                        quit()
                                        pygame.quit()
                                    else:
                                        data = "WIN"
                                        data = pickle.dumps(data)
                                        tcpClient.send(data)
                                        end_screen(win, "Black Win")
                                        time.sleep(3)
                                        tcpClient.close()
                                        quit()
                                        pygame.quit()
                                else:
                                    # print("Change and previous", change, prev_mv)
                                    #timeGone = int(time.time() - startTime)
                                    curr = (i,j)
                                    data_send = (prev_mv, curr, color)
                                    data_send = pickle.dumps(data_send)
                                    tcpClient.send(data_send)
                                    startTime = time.time() # if made move reset time
                                    if turn == "w":
                                        turn = "b"
                                    else:
                                        turn = "w"
                                    myTurn = False
                                    # print("MyTurn color: ", myTurn, turn)

                    try:
                        data = tcpClientA.recv(BUFFER_SIZE)
                        data = pickle.loads(data)
                        if data == "EXIT":
                            quit()
                            tcpClient.close()
                            pygame.quit()
                            sys.exit(0)
                    except socket.timeout:
                        pass

                else:
                    try:
                        data = tcpClient.recv(BUFFER_SIZE)

                        data = pickle.loads(data)
                        # print("Data received", data)

                        if isinstance(data,str):
                            if data == "WIN":
                                if turn == "w":
                                    end_screen(win, "White WIN")
                                else:
                                    end_screen(win, "Black WIN")
                                time.sleep(3)
                                tcpClient.close()
                                quit()
                                pygame.quit()
                                sys.exit(0)
                            if data == "EXIT":
                                quit()
                                tcpClient.close()
                                pygame.quit()

                        prev, curr, color_recv = data
                        # print("DATA RECEIVED: ", data)
                        bo.update_moves()
                        change = bo.move(prev, (curr[1], curr[0]),turn)
                        # print("Changed", change)
                        bo.update_moves()
                        bo.reset_selected()
                        if change:
                            # timeGone = int(time.time() - startTime)
                            startTime = time.time()  # if made move reset time
                            if turn == "w":
                                turn = "b"
                            else:
                                turn = "w"
                            if color_recv == 'white':
                                turn = "b"
                            else:
                                turn = "w"
                            myTurn = True
                            # print("MyTurn color: ", myTurn, turn)
                    except socket.timeout:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                                data = "EXIT"
                                data = pickle.dumps(data)
                                tcpClient.send(data)
                                tcpClient.close()
                                quit()  # quit app at all
                                pygame.quit()

            menu_screen(win)



        width = 750
        height = 750

        win = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Chess Game")
        menu_screen(win)