from human import Human
from bot import Bot
from state import State
from connection import Connection
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

SPEED_FACTOR = 0.5
DELTA_T = 0.02
FINAL_T = 10

bots = []
humans = []
modelStates = []
modelConnections = []

# Some parameters (weight of connections) of the model
OPENNESS = 0.7
W_EFFECT_OF_SUPPORT = -0.4184
W_STRESS_TO_SENDING_MESSAGE = 1
W_READING_MESSAGE_TO_SENDING_SUPPORT = 1
W_SENDING_MESSAGE_TO_MESSAGE = 1
W_SENDING_SUPPORT_TO_SUPPORT = 1
W_MESSAGE_TO_MESSAGE = 1
W_SUPPORT_TO_SUPPORT = 1
W_MESSAGE_TO_READING_MESSAGE = 1
W_SUPPORT_TO_RECEIVING_SUPPORT = 1


# Connecting a bot to a human
def connectBotToHuman(bot, human):
    # human sends message to bot
    hsmb = State('SM'+human.name+'to'+bot.name,
                 State.dictionaryOfFunctions[3])
    human.states.append(hsmb)
    # bot reads message from human
    brmh = State('RM'+bot.name+'from'+human.name,
                 State.dictionaryOfFunctions[0])
    bot.states.append(brmh)
    # bot sends support to human
    bssh = State('SS'+bot.name+'to'+human.name,
                 State.dictionaryOfFunctions[5])
    bot.states.append(bssh)
    # human reads support from bot
    hrsb = State('RS'+human.name+'from'+bot.name,
                 State.dictionaryOfFunctions[0])
    human.states.append(hrsb)
    # message from human to bot
    mhb = State('M'+human.name+'to'+bot.name,
                State.dictionaryOfFunctions[1])
    modelStates.append(mhb)
    # support from bot to human
    sbh = State('S'+bot.name+'to'+human.name,
                State.dictionaryOfFunctions[1])
    modelStates.append(sbh)

    # connection from human.stress to hsmb
    c1 = Connection('w_stress-hsmb', human.stress, hsmb,
                    W_STRESS_TO_SENDING_MESSAGE)
    human.connections.append(c1)
    # connection from hsmb to mhb
    c2 = Connection('w_hsmb-mhb', hsmb, mhb,
                    W_SENDING_MESSAGE_TO_MESSAGE)
    modelConnections.append(c2)
    # connection from mhb to mhb
    c3 = Connection('w_mhb-mhb', mhb, mhb,
                    W_MESSAGE_TO_MESSAGE)
    modelConnections.append(c3)
    # connection mhb to brmh
    c4 = Connection('w_mhb-brmh', mhb, brmh,
                    W_MESSAGE_TO_READING_MESSAGE)
    modelConnections.append(c4)
    # connection from brmh to bssh
    c5 = Connection('w_brmh-bssh', brmh, bssh,
                    W_READING_MESSAGE_TO_SENDING_SUPPORT)
    bot.connections.append(c5)
    # connection from bssh to sbh
    c6 = Connection('w_bssh-sbh', bssh, sbh,
                    W_SENDING_SUPPORT_TO_SUPPORT)
    modelConnections.append(c6)
    # connection from sbh to sbh
    c7 = Connection('w_mhb-mhb', sbh, sbh,
                    W_SUPPORT_TO_SUPPORT)
    modelConnections.append(c7)
    # connection from sbh to hrsb
    c8 = Connection('w_sbh-hrsb', sbh, hrsb,
                    W_SUPPORT_TO_RECEIVING_SUPPORT)
    modelConnections.append(c8)
    # connection from hrsb to human.stress
    c9 = Connection('w_hrsb-stress', hrsb, human.stress,
                    OPENNESS * W_EFFECT_OF_SUPPORT)
    human.connections.append(c9)


b1 = Bot("B1")
bots.append(b1)
h1 = Human("H1")
humans.append(h1)
h2 = Human("H2")
humans.append(h2)
h3 = Human("H3")
humans.append(h3)
h4 = Human("H4")
humans.append(h4)

connectBotToHuman(b1, h1)
connectBotToHuman(b1, h2)
connectBotToHuman(b1, h3)
connectBotToHuman(b1, h4)

for b in bots:
    modelStates.extend(b.states)
    modelConnections.extend(b.connections)

for h in humans:
    modelStates.extend(h.states)
    modelConnections.extend(h.connections)

b1SupportingH1 = []
b1SupportingH2 = []
b1SupportingH3 = []
b1SupportingH4 = []
h1Stress = []
h1AskingForSupport = []
h1ReceivingSupport = []
h2Stress = []
h2AskingForSupport = []
h2ReceivingSupport = []
h3Stress = []
h3AskingForSupport = []
h3ReceivingSupport = []
h4Stress = []
h4AskingForSupport = []
h4ReceivingSupport = []

t = 0.00
time = []
h1.negativeEvent.value = 0.7
while t <= FINAL_T:
    if t == 1:
        h1.negativeEvent.value = 0.7
    if t == 3:
        h2.negativeEvent.value = 0.7
    if t == 5:
        h3.negativeEvent.value = 0.7
    if t == 7:
        h4.negativeEvent.value = 0.7
    for s in modelStates:
        connectedStates = []
        connections = []
        for c in modelConnections:
            if c.toState == s:
                connectedStates.append(c.fromState)
                connections.append(c)
        s.updateValue(modelStates, connectedStates, connections,
                      SPEED_FACTOR, DELTA_T)
    t = t + DELTA_T
    t = round(t, 2)
    time.append(float(t))
    h1Stress.append(h1.stress.value)
    h2Stress.append(h2.stress.value)
    h3Stress.append(h3.stress.value)
    h4Stress.append(h4.stress.value)
    for s in modelStates:
        if s.name == 'SSB1toH1':
            b1SupportingH1.append(s.value)
        if s.name == 'SSB1toH2':
            b1SupportingH2.append(s.value)
        if s.name == 'SSB1toH3':
            b1SupportingH3.append(s.value)
        if s.name == 'SSB1toH4':
            b1SupportingH4.append(s.value)
        if s.name == 'SMH1toB1':
            h1AskingForSupport.append(s.value)
        if s.name == 'SMH2toB1':
            h2AskingForSupport.append(s.value)
        if s.name == 'SMH3toB1':
            h3AskingForSupport.append(s.value)
        if s.name == 'SMH4toB1':
            h4AskingForSupport.append(s.value)
        if s.name == 'RSH1fromB1':
            h1ReceivingSupport.append(s.value)
        if s.name == 'RSH2fromB1':
            h2ReceivingSupport.append(s.value)
        if s.name == 'RSH3fromB1':
            h3ReceivingSupport.append(s.value)
        if s.name == 'RSH4fromB1':
            h4ReceivingSupport.append(s.value)

plt.subplot(5, 1, 1).get_xaxis().set_visible(False)
plt.plot(b1SupportingH1)
plt.plot(b1SupportingH2)
plt.plot(b1SupportingH3)
plt.plot(b1SupportingH4)
plt.ylabel('B1')
plt.ylim(-0.1, 1.1)
fontP = FontProperties()
fontP.set_size('small')
plt.legend(['Helping H1', 'Helping H2', 'Helping H3', 'Helping H4'],
           prop=fontP, loc='upper left')

plt.subplot(5, 1, 2).get_xaxis().set_visible(False)
plt.plot(time, h1Stress)
plt.plot(time, h1AskingForSupport)
plt.plot(time, h1ReceivingSupport)
plt.ylabel('H1')
plt.ylim(-0.1, 1.1)
fontP = FontProperties()
fontP.set_size('small')
plt.legend(['Stress', 'Asking for Help', 'Receiving Support'],
           prop=fontP, loc='upper left')

plt.subplot(5, 1, 3).get_xaxis().set_visible(False)
plt.plot(time, h2Stress)
plt.plot(time, h2AskingForSupport)
plt.plot(time, h2ReceivingSupport)
plt.ylabel('H2')
plt.ylim(-0.1, 1.1)
fontP = FontProperties()
fontP.set_size('small')
plt.legend(['Stress', 'Asking for Help', 'Receiving Support'],
           prop=fontP, loc='upper left')

plt.subplot(5, 1, 4).get_xaxis().set_visible(False)
plt.plot(time, h3Stress)
plt.plot(time, h3AskingForSupport)
plt.plot(time, h3ReceivingSupport)
plt.ylabel('H3')
plt.ylim(-0.1, 1.1)
fontP = FontProperties()
fontP.set_size('small')
plt.legend(['Stress', 'Asking for Help', 'Receiving Support'],
           prop=fontP, loc='upper left')

plt.subplot(5, 1, 5)
plt.plot(time, h4Stress)
plt.plot(time, h4AskingForSupport)
plt.plot(time, h4ReceivingSupport)
plt.ylabel('H4')
plt.xlabel('Time')
plt.ylim(-0.1, 1.1)
fontP = FontProperties()
fontP.set_size('small')
plt.legend(['Stress', 'Asking for Help', 'Receiving Support'],
           prop=fontP, loc='upper left')

plt.show()
