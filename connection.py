class Connection():
    """This class represents a link between 2 given nodes (states)
    of the model. It contains a weight value which indicates how
    strong is the influence that one state exerts on the other."""
    def __init__(self, name, fromState, toState, weight):
        self.name = name
        self.fromState = fromState
        self.toState = toState
        self.weight = weight
