from core import event_handler
import socket

import wiringpi as wp
import gpioexp

wp.wiringPiSetup()
exp = gpioexp.gpioexp()

class LEDToggleHandler(event_handler.EventHandler):
    pin: int

    def __init__(self, pin: int) -> None:
        super().__init__()
        self.pin = pin
        wp.pinMode(pin, 1)

    def handle(self, value: str, connection: socket.socket):
        wp.digitalWrite(self.pin, int(value))

class LEDDimHandler(event_handler.EventHandler):
    pin: int

    def __init__(self, pin: int) -> None:
        super().__init__()
        self.pin = pin

    def handle(self, value: str, connection: socket.socket):
        exp.analogWrite(6, float(value) / 1023.0)
