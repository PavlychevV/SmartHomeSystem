import socket

class EventHandler():
    def __init__(self) -> None:
        pass

    def handle(self, value: str, connection: socket.socket):
        pass

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