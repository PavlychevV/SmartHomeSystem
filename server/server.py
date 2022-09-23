import atexit
from fileinput import close
import os
import pickle
from re import L
import socket
from threading import Thread
from core import event_handler
#from core import gpio_event_handler

# Установите соответствие между IP-адресом и обработчиком событий
handlers = {
    "192.168.1.87": event_handler.LightRemoteToggleHandler()
}

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

HOST = s.getsockname()[0]
PORT = 62302

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

atexit.register(lambda: {
    print("Closing socket..."),
    sock.close(),
    print("Server stopped")
})

sock.bind((HOST, PORT))
sock.listen(5)
print("Listening on port", PORT, "ip", HOST)

def handle_client(connection: socket.socket, address):
    while True:
        try:
            data = connection.recv(100)
            if not data:
                break

            newData = data.decode("utf-8").split("\r\n")

            for line in newData:
                if line == "":
                    continue

                handlers.get(address[0]).handle(line, connection)

        except socket.timeout:
            print("Connection timeout")
            connection.shutdown(socket.SHUT_RDWR)
            break
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            break

while True:
    print(f"Waiting for clients...")

    try:
        connection, address = sock.accept()
        print(f"Connected by {address} ")

        connection.settimeout(60)

        Thread(target=handle_client, args=(connection, address)).start()

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        break
    except:
        print("Error accepting connection")
