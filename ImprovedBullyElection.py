import random
import wsnsimpy.wsnsimpy_tk as wsp
from enum import Enum

ELECTION_STARTER = 0
SIZE = 500
MSG_COUNTER = 0

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
    def __init__(self, type=BullyMsgType.ELECTION, src="", dst="", data=0, path=[], sequence=0, version = 1) -> None:
        self.type = BullyMsgType(type)
        self.src = src
        self.dst = dst
        self.data = data

###########################################################
# for unit testing:
def bestCandidate(selfID, neighborIDs):
    res = []
    for n in neighborIDs:
        if n > selfID:
            res.append(n)
    return res

###########################################################
class MyNode(wsp.Node):
    tx_range = 100

    ##################
    def init(self):
        super().init()
        self.bestOK = self.id
        self.leader = None

    ##################
    def run(self):
        if self.id == ELECTION_STARTER:
            self.scene.nodecolor(self.id,0,0,0)
            self.recv = True
            yield self.timeout(0.5)
            self.election()
        else:
            self.scene.nodecolor(self.id,.7,.7,.7)

    ##################
    def election(self):
        self.bestOK = self.id
        elecMsg = BullyMsg(BullyMsgType.ELECTION, src=self.id, data="")
        nodes = []
        for n in self.neighbors:
            nodes.append(n.id)
        candidates = bestCandidate(self.id, nodes)
        for n in candidates:
            self.send(n, msg = elecMsg)

        self.sim.delayed_exec(delay=0.5, func=self.coordinator)

    ######################
    def coordinator(self):
        coordMsg = BullyMsg(BullyMsgType.COORDINATOR, src=self.id, data=self.bestOK)
        self.leader = self.bestOK
        self.send(wsp.BROADCAST_ADDR, msg = coordMsg)    

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
        if msg.type == BullyMsgType.OK:
            self.log(f"{MSG_COUNTER} OK from {sender}")
            if(sender > self.bestOK):
                self.bestOK = sender
        if msg.type == BullyMsgType.COORDINATOR:
            self.log(f"{MSG_COUNTER} COORDINATOR: {msg.data} from {sender}")
            self.leader = msg.data
        self.scene.nodecolor(self.id,1,0,0)
        yield self.timeout(random.uniform(0.5,1.0))
        
###########################################################
if __name__ == '__main__':
    sim = wsp.Simulator(
            until=100,
            timescale=1,
            visual=True,
            terrain_size=(SIZE,SIZE),
            title="Improved Bully Election")
    for x in range(3):
        for y in range(3):
            px = 50 + x*200
            py = 50 + y*200
            node = sim.add_node(MyNode, (px,py))
            node.tx_range = 2*SIZE
            node.logging = True
    sim.run()
