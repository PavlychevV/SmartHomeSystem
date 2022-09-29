class Event():
    name = "Event"
    def __init__(self, name) -> None:
        self.name = name

class LightsEvent(Event):
    name = "Lights"
    state = False

    def __init__(self, state) -> None:
        self.state = state
