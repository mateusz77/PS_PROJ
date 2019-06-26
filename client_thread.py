import socket
import pickle
import struct

from config import *

host = SERVER_ADDRESS
port = SERVER_PORT

buffer_size = BUFFER_SIZE

servers = []

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

    if message == "You are client A":
        while message != "exit":
            message = input("Enter message or enter exit")
            if message == "exit":
                break
            message = pickle.dumps(message)
            tcpClientA.send(message)
            data = tcpClientA.recv(buffer_size)
            data = pickle.loads(data)
            print("Client received data: ", data)

    else:
        while message != "exit":
            data = tcpClientA.recv(buffer_size)
            data = pickle.loads(data)
            print("Client received data: ", data)
            message = input("Enter message or enter exit")
            if message == "exit":
                break
            message = pickle.dumps(message)
            tcpClientA.send(message)

    tcpClientA.close()
