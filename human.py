from state import State
from connection import Connection


class Human():
    """This class represents a Human. It contains a set of internal states and
    connections."""
    def __init__(self, name):
        self.name = name
        self.states = []
        self.connections = []

        # Internal states of a human being.
        self.positiveEvent = State(name+"_e+")
        self.negativeEvent = State(name+"_e-")
        self.stress = State(name+"_st", State.dictionaryOfFunctions[2])
        self.emotionalResources = State(
            name+"_er", State.dictionaryOfFunctions[2]
        )
        self.states.append(self.positiveEvent)
        self.states.append(self.negativeEvent)
        self.states.append(self.stress)
        self.states.append(self.emotionalResources)

        # Internal connections between the internal states.
        self.connections.append(
            Connection("w1_"+self.name, self.negativeEvent, self.stress, 1))
        self.connections.append(
            Connection("w2_"+self.name, self.positiveEvent,
                       self.emotionalResources, 1))
        self.connections.append(
            Connection("w3_"+self.name, self.stress,
                       self.emotionalResources, -1))
