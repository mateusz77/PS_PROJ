import socket
import sys
import threading
import pickle
import random
import time

from config import *

# To get access to the list of players
global lock1
lock1 = threading.Lock()

global lock2
lock2 = threading.Lock()


# List of players
players = []
""" List of dictionaries
    {'playerID': int,
     'enemyID' : int,
     'inGame' : bool,
    }
"""

conns = []

def handle_players():
    print("HANDLE PLAYER LOOP")
    while True:
        try:
            with lock1:
                conn = conns.pop()
            client_sock, client_address = conn
            msg = client_sock.recv(BUFFER_SIZE)
            print("Client:", client_address, "INDEX GRANTING")
            # If it is occupied - random int
            idAccepted = False
            playerID = pickle.loads(msg)
            while not idAccepted:
                playerID = random.randint(0, 150)
                with lock2:
                    for p in players:
                        if p['playerID'] == playerID:
                            continue
                    idAccepted = True

            print("Client:", client_address, "INDEX GRANTED")
            # Create and save the player
            playerData = {
                "playerID": playerID,
                "enemyID": -1,
                "sock": client_sock,
                "inGame": False,
                "isSecond": False,
            }

            with lock2:
                print("HANDLE PLAYER - PLAYER APPENDED")
                players.append(playerData)

            time.sleep(0.9)
        except IndexError:
            pass
        except socket.error as e:
            # Catch socket errors and finish thread.
            print("Socket error {0}: {1}".format(e.errno, e.strerror))
            return

def create_game():
    game_list = []
    print("GREATE GAME LOOP")
    while True:
        try:
            client_a = None
            client_b = None


            with lock2:
                print("LENGTH OF THE LIST - ", len(players))
                print("GREATE GAME - LOOK FOR A PLAYER_1")
                for i, player in players:
                    if player["inGame"] == False:
                        client_a = player

                print("GREATE GAME - LOOK FOR A PLAYER_2")
                for i, player in players:
                    if player["playerID"] != client_a["playerID"]:
                        if player["inGame"] == False:
                            print("GREATE GAME - GAME INITIALIZATION")
                            client_b = player

                            client_a["enemyID"] = client_b["playerID"]
                            client_b["enemy_ID"] = client_a["playerID"]

                            client_a["inGame"] = client_b["inGame"] = True

                            client_b["isSecond"] = True

                            game_thread = threading.Thread(target=start_game, args=(client_a, client_b))
                            game_list.append(game_thread)
                            game_thread.start()
                        break
            time.sleep(1)

        except:

            for game in game_list:
                game.join()
            sys.exit(1)

def start_game(client_a, client_b):
    print("START GAME THREAD")

    client_a_sock = client_a["sock"]
    client_b_sock = client_b["sock"]

    gameIsRunning = True

    data = "You are client A"
    data = pickle.dumps(data)
    client_a_sock.send(data)

    data = "You are client B"
    data = pickle.dumps(data)
    client_b_sock.send(data)

    while gameIsRunning:
        try:
            data_to_b = client_a_sock.recv(BUFFER_SIZE)
            data_to_b = pickle.loads(data_to_b)

            if data_to_b:

                print("Data to client B: ", data_to_b)

                data_to_b = pickle.dumps(data_to_b)
                client_b_sock.send(data_to_b)
            else:
                print("Client disconnected")
                raise Exception('Client disconnected')

            data_to_a = client_b_sock.recv(BUFFER_SIZE)
            data_to_a = pickle.loads(data_to_a)

            if data_to_a:

                print("Data to client A: ", data_to_a)

                data_to_a = pickle.dumps(data_to_a)
                client_a_sock.send(data_to_a)
            else:
                print("Client disconnected")
                raise Exception('Client disconnected')
        except:
            client_a_sock.close()
            client_b_sock.close()

            lock2.acquire()
            rm_idx = None

            for i, p in enumerate(players):
                if p["playerID"] == client_a["playerID"]:
                    rm_idx = i
                    break

            players.pop(rm_idx)
            for i, p in enumerate(players):
                if p["playerID"] == client_b["playerID"]:
                    rm_idx = i
                    break
            players.pop(rm_idx)
            lock2.release()

            gameIsRunning = False

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        print("Started listening to client")
        self.sock.listen(5)
        thread_list = []
        handle_players_thread = threading.Thread(target=handle_players)
        create_game_thread = threading.Thread(target=create_game)

        handle_players_thread.start()
        create_game_thread.start()
        try:
            while True:
                print("Listening")
                client, address = self.sock.accept()
                print("Connection from client:", address)
                client.settimeout(60)
                player = (client,address)
                with lock1:
                    conns.append(player)

        except socket.error as e:
            # Catch socket errors.
            print("Socket error {0}: {1}".format(e.errno, e.strerror))
        except Exception as e:
            # Catch other errors.
            print("Exception {0}: {1}".format(type(e).__name__, e))

            create_game_thread.terminate()
            handle_players_thread.terminate()

            create_game_thread.join()
            handle_players_thread.join()
            sys.exit(1)




if __name__ == "__main__":
    ThreadedServer(SERVER_ADDRESS, SERVER_PORT).listen()
