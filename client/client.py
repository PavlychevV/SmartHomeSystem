import socket

HOST: str = "192.168.1.79"
PORT: int = 62302

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    while True:
        sock.sendall(input("Input sending data: ").encode("utf-8"))