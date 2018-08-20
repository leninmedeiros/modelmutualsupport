class State():
    """This class represents a state. It can be either an input or a transitional
    state. Input states can be seen as triggers that start the computation of
    the model. They are used as parameters, then they remain constant over time
    unless the user decides to change their values. Transitional states have
    values automatically computed every time step. Such a computation is in
    accordance with the respective combination function."""

    dictionaryOfFunctions = ['id', 'max', 'scaled_sum', 'threshold',
                             'support_logic_1', 'support_logic_2']

    def __init__(self, name, combinationFunction=None, value=0):
        self.name = name
        self.combinationFunction = combinationFunction
        self.value = value

    def updateValue(self, modelStates,
                    states, connections, speedFactor, deltaT):
        states.sort(key=lambda state: state.name)
        connections.sort(key=lambda connection: connection.fromState.name)
        newValue = 0
        if self.combinationFunction is not None:
            if self.combinationFunction == State.dictionaryOfFunctions[0]:
                newValue = State.id(self, states, connections)
            if self.combinationFunction == State.dictionaryOfFunctions[1]:
                newValue = State.max(self, states, connections)
            if self.combinationFunction == State.dictionaryOfFunctions[2]:
                newValue = State.scaledSum(self, states, connections,
                                           speedFactor, deltaT)
            if self.combinationFunction == State.dictionaryOfFunctions[3]:
                newValue = State.threshold(self, states, connections)
            if self.combinationFunction == State.dictionaryOfFunctions[4]:
                newValue = State.supportLogic1(self, states, connections)
            if self.combinationFunction == State.dictionaryOfFunctions[5]:
                newValue = State.supportLogic2(self, states, connections,
                                               modelStates)
            if newValue < 0:
                self.value = 0
            elif newValue > 1:
                self.value = 1
            else:
                self.value = newValue

    def id(self, states, connections):
        return states[0].value * connections[0].weight

    def max(self, states, connections):
        v1 = states[0].value * connections[0].weight
        v2 = states[1].value * connections[1].weight
        listToCheck = [v1, v2]
        return max(listToCheck)

    def scaledSum(self, states, connections, speedFactor, deltaT):
        factors = []
        factorTemp = 0
        for s in states:
            factorTemp = s.value * connections[states.index(s)].weight
            factors.append(factorTemp)
        dividend = 0
        divisor = 0
        division = 0
        for f in factors:
            dividend = dividend + f
        for c in connections:
            if c.weight > 0:
                divisor = divisor + c.weight
        if divisor > 0:
            division = dividend / divisor
        valueToReturn = speedFactor * (division - self.value) * deltaT
        valueToReturn = self.value + valueToReturn
        return valueToReturn

    def threshold(self, states, connections):
        THRESHOLD = 0.5
        if states[0].value * connections[0].weight > THRESHOLD:
            return 1
        else:
            return 0

    def supportLogic1(self, states, connections):
        return False

    def supportLogic2(self, states, connections, modelStates):
        stringTemp = self.name.replace("SS", "")
        stringTemp = stringTemp.replace("to", ",")
        stringTemp = stringTemp.split(",")
        support = None
        valueToReturn = self.value
        for s in modelStates:
            if s.name == 'S'+stringTemp[0]+'to'+stringTemp[1]:
                support = s
        if states[0].value*connections[0].weight == 1 and support.value == 0:
            valueToReturn = 1
        return valueToReturn
