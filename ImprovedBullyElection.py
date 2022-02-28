import random
import wsnsimpy.wsnsimpy_tk as wsp
from enum import Enum

ELECTION_STARTER = 0
SIZE = 500

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
class MyNode(wsp.Node):
    tx_range = 100

    ##################
    def init(self):
        super().init()
        self.OKreplies = [] # To hold IDs of responding nodes when holding election
        self.leader = None

    ##################
    def run(self):
        if self.id == ELECTION_STARTER:
            self.scene.nodecolor(self.id,0,0,0)
            self.recv = True
            yield self.timeout(2)
            self.election()
        else:
            self.scene.nodecolor(self.id,.7,.7,.7)

    ##################
    def election(self):
        self.OKreplies = []
        elecMsg = BullyMsg(BullyMsgType.ELECTION, src=self.id, data="")
        self.send(wsp.BROADCAST_ADDR, msg = elecMsg)        
        #self.log(f"env: {self.sim.env}")
        #timeout = self.sim.env.timeout(delay = 1)
        #yield timeout
        #self.log(f"Waited for timeout, got OKs from: {self.OKreplies}")

    ##################
    def broadcast(self):
        self.scene.nodewidth(self.id, len(self.neighbors))
        self.send(wsp.BROADCAST_ADDR)

    ##################
    def on_receive(self, sender, msg, **kwargs):
        self.log(f"Receive message from {sender}")
        if msg.type == BullyMsgType.ELECTION:
            self.log(f"Message was ELECTION")
            if self.id > sender:
                self.log(f"I will reply OK")
                okMsg = BullyMsg(BullyMsgType.OK, src=self.id, data="")
                self.send(sender, okMsg)
        if msg.type == BullyMsgType.OK:
            self.log(f"Message was OK")
            self.OKreplies.append(sender)
        if msg.type == BullyMsgType.COORDINATOR:
            self.log(f"Message was COORDINATOR")
            self.leader = sender
        self.scene.nodecolor(self.id,1,0,0)
        yield self.timeout(random.uniform(0.5,1.0))
        
###########################################################
sim = wsp.Simulator(
        until=100,
        timescale=1,
        visual=True,
        terrain_size=(SIZE,SIZE),
        title="Flooding Demo")
for x in range(2):
    for y in range(2):
        px = 100 + x*200
        py = 100 + y*200
        node = sim.add_node(MyNode, (px,py))
        node.tx_range = SIZE
        node.logging = True
sim.run()
