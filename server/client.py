import socket
import pickle
from core import event

HOST = "127.0.0.1"
PORT = 60123

ev = event.LightsEvent(True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
    socket.connect((HOST, PORT))

    while True:
        socket.sendall(pickle.dumps(ev))
        data = socket.recv(1024)

        print(f"Received {data!r}")