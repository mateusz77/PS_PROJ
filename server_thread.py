import socket
import sys
import threading
import pickle
import random
import time
import struct
import logging
import logging.handlers

from config import *
from daemon import *

# To get access to the list of players
global lock
lock = threading.Lock()

# List of players
players = []
""" List of dictionaries
    {'playerID': int,
     'enemyID' : int,
     'inGame' : bool,
    }
"""
# Logging definition
logging.basicConfig(
    filename="./log/server.log",
    format='%(asctime)-6s:%(threadName)-8s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=LOGIN_LEVEL
)

def signal_handler(sig, frame):
    # print('Closing connection.')
    logging.info("Closing connections.")
    with lock:
        for conn in players:
            conn["sock"].close()
    exit()


def mcast_daemon():
    while True:
        try:
            server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_udp_tuple = (SERVER_ADDRESS, SERVER_PORT)
            server_udp.bind(server_udp_tuple)
            group = socket.inet_aton(MCAST_GROUP)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            server_udp.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            logging.info("Socket UDP for port {} created and binded.".format(SERVER_PORT))
            # print("Socket UDP for port 6060 created and binded.")

        except:
            logging.error("Socket UDP for port {} couldn't be created or binded".format(SERVER_PORT))
            # print("Socket UDP for port 6060 couldn't be created or binded")

        data, address = server_udp.recvfrom(1024)
        print("Received multicast data from {}".format(address))
        server_udp.sendto('server-ack'.encode(), address)


def handle_player(client_sock, addr):
    global lock
    # Read Player ID
    # print("Client:", addr, "INITIALIZE")
    logging.info("Client: {} INITIALIZE".format(addr))
    try:
        msg = client_sock.recv(BUFFER_SIZE)
    except socket.error as e:
        # Catch socket errors and finish thread.
        # print("Socket error {0}: {1}".format(e.errno, e.strerror))
        logging.error("Socket error {0}: {1}".format(e.errno, e.strerror))
        return

    # print("Client:", addr, "INDEX GRANTING")
    # logging.info(f"Client: {addr} INDEX GRANTING")
    logging.info("Client: {} INDEX GRANTING".format(addr))
    client_a = client_sock

    # If it is occupied - random int
    idAccepted = False
    playerID = pickle.loads(msg)
    while not idAccepted:
        playerID = random.randint(0, 150)
        lock.acquire()
        for p in players:
            if p['playerID'] == playerID:
                continue
        idAccepted = True
        lock.release()

    # print("Client:", addr, "INDEX GRANTED")
    # logging.info(f"Client: {addr} INDEX GRANTED")
    logging.info("Client: {} INDEX GRANTED".format(addr))

    # Create and save the player
    playerData = {
        "playerID": playerID,
        "enemyID": -1,
        "sock": client_sock,
        "inGame": False,
        "isSecond": False,
    }

    with lock:
        players.append(playerData)

    # Look for other player
    client_b = None

    # print("Client:", addr, "WAIT FOR THE PLAYER")
    # logging.info(f"Client: {addr} WAIT FOR THE PLAYER")
    logging.info("Client: {} WAIT FOR THE PLAYER".format(addr))


    while not playerData["inGame"]:
        with lock:
            # print("LENGTH OF PLAYER LIST:", len(players))
            # logging.info(f"LENGTH OF PLAYER LIST: {len(players)}")
            logging.info("LENGTH OF PLAYER LIST: {}".format(len(players)))

            for i, p in enumerate(players):
                if not p["inGame"] and p["playerID"] != playerData["playerID"]:
                    # print("Client:", addr, "PLAYER GRANTED")
                    logging.info("Client:", addr, "PLAYER GRANTED")
                    playerData["enemyID"] = p["playerID"]
                    p["enemyID"] = playerData["playerID"]
                    playerData["inGame"] = True
                    p["inGame"] = True
                    p["isSecond"] = True
                    client_b = p["sock"]
                    break
                else:
                    # print("Waiting for the player")
                    logging.info("Waiting for the player")
        time.sleep(1)

    # Two parallel threads
    if playerData["isSecond"] == True:
        with lock:
            for i, p in enumerate(players):
                if p["playerID"] == playerData["enemyID"]:
                    client_b = p["sock"]
                    break

    # print("Client:", addr, "IS SECOND: ", playerData["isSecond"])
    # logging.info(f"Client: {addr}, IS SECOND: , {playerData['isSecond']}")
    logging.info("Client: {}, IS SECOND: , {}".format(addr, playerData['isSecond']))

    # Start the game
    gameIsRunning = True

    ########################################################################
    ########################### PROPER GAME ################################
    ########################################################################
    # TODO: CHANGE THIS SECTION FOR A GAME NOT FOR A CHAT
    # Inform which client starts the conversation
    if not playerData["isSecond"]:
        data = "white"
        data = pickle.dumps(data)
        client_a.send(data)

        data = "black"
        data = pickle.dumps(data)
        client_b.send(data)

    while True:
        if not playerData["isSecond"]:
            # print("Client:", addr, "CONNECTION ESTABLISHED")
            # logging.info("Client:", addr, "CONNECTION ESTABLISHED")
            logging.info("Client: {} CONNECTION ESTABLISHED".format(addr))
            while gameIsRunning:
                try:
                    try:
                        data_to_b = client_a.recv(BUFFER_SIZE)
                        data_to_b = pickle.loads(data_to_b)

                        if data_to_b:

                            # print("Data to client B: ", data_to_b)
                            # logging.info(f"Data to client B: {data_to_b}")
                            logging.info("Data to client B: {}".format(data_to_b))
                            data_to_b = pickle.dumps(data_to_b)
                            client_b.send(data_to_b)
                        else:

                            # print("Client disconnected")
                            logging.error("Client A disconnected")
                            raise Exception('Client A disconnected')
                    except socket.timeout:
                        pass

                    try:
                        data_to_a = client_b.recv(BUFFER_SIZE)
                        data_to_a = pickle.loads(data_to_a)

                        if data_to_a:

                            # print("Data to client A: ", data_to_a)
                            # logging.info(f"Data to client A: {data_to_a}")
                            logging.info("Data to client A: {}".format(data_to_a))

                            data_to_a = pickle.dumps(data_to_a)
                            client_a.send(data_to_a)
                        else:
                            # print("Client disconnected")
                            logging.error("Client B disconnected")
                            raise Exception('Client B disconnected')
                    except socket.timeout:
                        pass
                except:
                    client_a.close()
                    client_b.close()

                    lock.acquire()
                    rm_idx = None

                    for i, p in enumerate(players):
                        if p["playerID"] == playerData["enemyID"]:
                            rm_idx = i
                            break

                    players.pop(rm_idx)
                    for i, p in enumerate(players):
                        if p["playerID"] == playerData["playerID"]:
                            rm_idx = i
                            break
                    players.pop(rm_idx)
                    lock.release()

                    gameIsRunning = False
            if not gameIsRunning:
                break
        else:
            if playerData is None:
                return
            return

    return


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        # print("Started listening to client")
        logging.info("Started listening to client")
        self.sock.listen(5)
        thread_list = []

        mcast_thread = threading.Thread(target=mcast_daemon)
        mcast_thread.start()

        signal.signal(signal.SIGINT, signal_handler)
        try:
            while True:
                # print("Listening")
                logging.info("Listening")
                client, address = self.sock.accept()
                # print("Connection from client:", address)
                # logging.info(f"Connection from client: {address}")
                logging.info("Connection from client: {}".format(address))

                client.settimeout(TIMEOUT+0.000001)
                thread_client = threading.Thread(target=self.listenToClient, args=(client, address)).start()
                thread_list.append(thread_client)

        except socket.error as e:
            # Catch socket errors.
            # print("Socket error {0}: {1}".format(e.errno, e.strerror))
            logging.error("Socket error {0}: {1}".format(e.errno, e.strerror))
        except Exception as e:
            # Catch other errors.
            # print("Exception {0}: {1}".format(type(e).__name__, e))
            logging.error("Exception {0}: {1}".format(type(e).__name__, e))

            mcast_thread.terminate()
            mcast_thread.join()

            for t in thread_list:
                t.join()
            sys.exit(1)

    def listenToClient(self, client, address):
        handle_player(client, address)


class ServerDaemon(Daemon):
    def run(self):
        ThreadedServer(SERVER_ADDRESS, SERVER_PORT).listen()


if __name__ == "__main__":
    daemon = ServerDaemon('/tmp/chess_daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
    # ThreadedServer(SERVER_ADDRESS, SERVER_PORT).listen()
