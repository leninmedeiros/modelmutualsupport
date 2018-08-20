class Bot():
    """This class represents a Bot. It contains a set of internal states and
    connections."""
    def __init__(self, name):
        self.name = name
        self.states = []
        self.connections = []
