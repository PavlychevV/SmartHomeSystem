import atexit
import socket
from threading import Thread
from typing import Optional, Tuple
from core import event_handler
#from core import gpio_event_handler

connections = [(socket.socket, (str, int))]

def get_connection(ip: str) -> Optional[tuple[socket.socket, (str, int)]]:
    for connection in connections:
        if connection[1][0] == ip:
            return connection

    return None

# Установите соответствие между IP-адресом и обработчиком событий
handlers: dict[str, event_handler.EventHandler] = {
    "192.168.1.79": event_handler.LightControlHandler(lambda: get_connection("192.168.1.87")),      # Этот компьютер
    "192.168.1.82": event_handler.BrightnessControlHandler(lambda: get_connection("192.168.1.87")), # ESP8266
    "192.168.1.87": event_handler.EventHandler(),                                                   # ESP32
}
# ESP8266 и этот компьютер будут отправлять данные на ESP32, которая, 
# в зависимости от полученных данных, будет управлять светом.

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

HOST: str = s.getsockname()[0]
PORT: int = 62302

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


def handle_client(connection: socket.socket, address: Tuple[str, int]):
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                break

            newData = data.decode("utf-8").split("\r\n")

            for line in newData:
                if line == "" or line == "OK":
                    continue
                
                handler = handlers.get(address[0])
                
                try:
                    handler.handle(line, connection)
                except BrokenPipeError:
                    print("Broken pipe")

                    if handler is event_handler.ControlHandler:
                        chandler: event_handler.ControlHandler = handler
                        connections.remove(chandler.get_connection())
        except socket.timeout:
            print("Connection timeout")
            connection.shutdown(socket.SHUT_RDWR)
            break
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            break
        except Exception as e:
            print("Connection reset:", e)
            connections.remove((connection, address))
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except:
                pass
            break


while True:
    print(f"Waiting for clients...")

    try:
        connection, address = sock.accept()

        connection.settimeout(5)

        for c in connections:
            if c[1][0] != address[0]:
                continue
            
            connections.remove(c)
            break

        connections.append((connection, address))
        print(f"Connected by {address}, total connections: {len(connections) - 1}")

        Thread(target=handle_client, args=(connection, address)).start()

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        break  
    except Exception as e:
        print("Connection reset:", e)
