from typing import Callable
import socket

class EventHandler():
    def __init__(self) -> None:
        pass

    def handle(self, value: str, connection: socket.socket):
        print("Connection", connection, "is handling", value)
        pass

class ControlHandler(EventHandler):
    get_connection: Callable[[str], tuple[socket.socket, (str, int)] | None]
    
    def __init__(self, get_connection: Callable[[str], tuple[socket.socket, (str, int)] | None]) -> None:
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
    get_connection: Callable[[str], tuple[socket.socket, (str, int)] | None]
    
    def __init__(self, get_connection: Callable[[str], tuple[socket.socket, (str, int)] | None]) -> None:
        super().__init__(get_connection)

    def handle(self, value: str, connection: socket.socket):
        intval = int(value)
        conn = self.get_connection()

        if conn == None:
            print("Connection not found")
            return

        handler = LightRemoteToggleHandler()

        try:
            handler.handle(intval, conn[0])
        except BrokenPipeError:
            print("Broken pipe")
