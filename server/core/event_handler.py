from datetime import datetime, timedelta
from typing import Callable, Optional, Tuple
import socket

class EventHandler():
    def __init__(self) -> None:
        pass

    def handle(self, value: str, connection: socket.socket):
        pass

class ControlHandler(EventHandler):
    get_connection: Callable[[], Optional[Tuple[socket.socket, Tuple[str, int]]]]
    
    def __init__(self, get_connection: Callable[[], Optional[Tuple[socket.socket, Tuple[str, int]]]]) -> None:
        super().__init__()
        self.get_connection = get_connection

class LightToggleHandler(EventHandler):
    def __init__(self) -> None:
        super().__init__()

    def handle(self, value: str, connection: socket.socket):
        print(f"Light is {('on' if bool(int(value)) else 'off')}")

class ClimatHandler(EventHandler):
    def __init__(self) -> None:
        super().__init__()

    def handle(self, value: str, connection: socket.socket):
        params = value.split(';')

        print(f"{params[0]} C, {params[1]}%")

class LightRemoteToggleHandler(EventHandler):
    def __init__(self) -> None:
        super().__init__()

    def handle(self, value: str, connection: socket.socket):
        intval = int(value)

        print(f"Light is {('on' if bool(int(intval)) else 'off')}")
        connection.send(f"{intval}\n".encode("utf-8"))

class LightControlHandler(ControlHandler):
    get_connection: Callable[[], Optional[Tuple[socket.socket, Tuple[str, int]]]]
    
    def __init__(self, get_connection: Callable[[], Optional[Tuple[socket.socket, Tuple[str, int]]]]) -> None:
        super().__init__(get_connection)

    def handle(self, value: str, connection: socket.socket):
        intval = int(value)
        conn: tuple[socket.socket, (str, int)] = self.get_connection()

        if conn == None:
            print("Connection not found")
            return

        handler = LightRemoteToggleHandler()

        handler.handle(intval, conn[0])

class BrightnessControlHandler(ControlHandler):
    brightness: int = 0
    get_connection: Callable[[], Optional[Tuple[socket.socket, Tuple[str, int]]]]
    last_sent_time: datetime = datetime.now()
    last_sent_brightness: int = 0
    
    def __init__(self, get_connection: Callable[[], Optional[Tuple[socket.socket, Tuple[str, int]]]]) -> None:
        super().__init__(get_connection)

    def handle(self, value: str, connection: socket.socket):
        brightness = self.brightness
        step = 1

        if bool(int(value)):
            brightness += step
        else:
            brightness -= step

        self.brightness = brightness = max(0, min(250, brightness))

        conn: tuple[socket.socket, (str, int)] = self.get_connection()

        if conn == None:
            print("Connection not found")
            return

        if datetime.now() - self.last_sent_time > timedelta(milliseconds=20) and self.last_sent_brightness != brightness:
            self.last_sent_time = datetime.now()
            self.last_sent_brightness = brightness
            conn[0].send(bytearray([brightness]))
            print(f"Brightness is {brightness}")
