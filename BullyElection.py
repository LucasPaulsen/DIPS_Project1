import random
import wsnsimpy.wsnsimpy_tk as wsp
from enum import Enum

ELECTION_STARTER = 0
SIZE = 500
MSG_COUNTER = 0
NO_OF_NODES = 9


def setElectionStarter(starter):
    global ELECTION_STARTER
    ELECTION_STARTER = starter


def clearMsgCount():
    global MSG_COUNTER
    MSG_COUNTER = 0


def getMsgCount():
    return MSG_COUNTER


def increment():
    global MSG_COUNTER
    MSG_COUNTER = MSG_COUNTER+1


class BullyMsgType(Enum):
    ELECTION = 1
    OK = 2
    COORDINATOR = 3


class BullyMsg:
    def __init__(self, type=BullyMsgType.ELECTION, src="", dst="", data=0, path=[], sequence=0, version=1) -> None:
        self.type = BullyMsgType(type)
        self.src = src
        self.dst = dst
        self.data = data

###########################################################


class MyNode(wsp.Node):
    tx_range = 100

    ##################
    def init(self):
        super().init()
        self.election_destinations = []
        self.bullied = False
        self.leader = None
        self.election_held = False

    ##################
    def run(self):
        if self.id == ELECTION_STARTER:
            self.scene.nodecolor(self.id, 0, 0, 0)
            self.recv = True
            yield self.timeout(0.7)
            self.election()
        else:
            self.scene.nodecolor(self.id, .7, .7, .7)

    ##################
    def election(self):
        self.bullied = False
        print(f'node #{self.id} is holding election START___________')
        elecMsg = BullyMsg(BullyMsgType.ELECTION,
                           src=self.id, data="")

        for n in self.neighbors:  # filter neighbors with higher ID
            if n.id > self.id:
                self.send(n.id, msg=elecMsg)

        self.election_held = True
        self.sim.delayed_exec(delay=0.5, func=self.coordinator)

    ######################

    def coordinator(self):
        if(not self.bullied):
            coordMsg = BullyMsg(BullyMsgType.COORDINATOR,
                                src=self.id, data="")
            self.leader = self.id
            print(f'NODE {self.id} is the new LEADER')
            self.send(wsp.BROADCAST_ADDR, msg=coordMsg)

    ##################
    def broadcast(self):
        self.scene.nodewidth(self.id, len(self.neighbors))
        self.send(wsp.BROADCAST_ADDR)

    ##################
    def on_receive(self, sender, msg, **kwargs):
        increment()
        if msg.type == BullyMsgType.ELECTION:
            self.log(f"{MSG_COUNTER} ELECTION from {sender}")
            if self.id > sender:
                okMsg = BullyMsg(BullyMsgType.OK, src=self.id, data="")
                self.send(sender, okMsg)
                if self.election_held is False:
                    self.election()

        if msg.type == BullyMsgType.OK:
            self.bullied = True
            self.log(f"{MSG_COUNTER} OK from {sender}")

        if msg.type == BullyMsgType.COORDINATOR:
            self.log(f"{MSG_COUNTER} COORDINATOR: {sender}")
            self.leader = sender
        self.scene.nodecolor(self.id, 1, 0, 0)

        yield self.timeout(random.uniform(0.5, 1.0))


###########################################################
if __name__ == '__main__':
    sim = wsp.Simulator(
        until=100,
        timescale=1,
        visual=True,
        terrain_size=(SIZE, SIZE),
        title="Bully Election")
    for x in range(4):
        for y in range(4):
            px = 50 + x*50
            py = 50 + y*50
            node = sim.add_node(MyNode, (px, py))
            node.tx_range = 2*SIZE
            node.logging = True
    sim.run()