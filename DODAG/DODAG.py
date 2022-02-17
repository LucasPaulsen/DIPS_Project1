import random
import wsnsimpy.wsnsimpy_tk as wsp
from anytree import Node, RenderTree, find_by_attr, AsciiStyle, find
import threading
from tools import cprint
import re
import json

ROOT = 6
# DEST   = 6
debug_cnt = 0
delayOn = True
pPackageLoss = 0.00  # Packet loss probability
trickleTimeInit = 1.5
batteryLevel = 100
DEBUG_MSG = False
from enum import Enum


class RPMType(Enum):
    DIO = 1
    DAO = 2
    DIS = 3
    DATA = 4
    ACK = 5


###########################################################
def delay():
    if delayOn:
        return random.uniform(.2, .8)
    else:
        return 0


class RPLMessage:
    def __init__(self, type=RPMType.DIO, src="", dst="", data=0, path=[], sequence=0, version = 1) -> None:
        self.type = RPMType(type)
        self.src = src
        self.dst = dst
        self.sequence = sequence
        self.data = data
        self.path = path
        self.version = version


###########################################################
class MyNode(wsp.Node):
    tx_range = 120
    version = 0
    trickleTime = trickleTimeInit
    trickleCount = 1
    rank = 0
    sequence_count = 0
    batteryLvl = batteryLevel
    tod = None #Time of death

    def batteryCheck(self):
        
        if self.batteryLvl <= 0:
            if self.tod is None:
                self.scene.nodecolor(self.id, 1, 0, 0)  #Colors node red when empty
                #self.tx_range = 0 
                #self.timeout(999)                      #Scuffed way of turning off node          
                self.tod = sim.now                      #Notes the time of death
                print("Node {}: TOD {}".format(self.id, self.tod))
        if self.id != ROOT:                             #Root node dosent have a battery, is hardwired
            self.batteryLvl -= 1                        #Cost of transmission
        if self.id == 13:
            print("Node {} >> Battery: {}".format(self.id, self.batteryLvl))    
        return self.batteryLvl

    ###################
    def init(self):
        super().init()
        self.prev = None
        self.rank = 0

    ###################
    # Startup command for each node
    # sets color of ROOT and destination node.
    def run(self):
        if self.id is ROOT:
            self.root = Node(str(self.id))
            self.prev = 0
            self.paths = []
            self.scene.nodecolor(self.id, 1, 0, 1)
            self.scene.nodewidth(self.id, 2)
            yield self.timeout(0)
            self.send_DIO()
            self.version = 1  # set root node version to 1 to enable it to send trickle messages
        # elif self.id is DEST:
        #    self.scene.nodecolor(self.id,1,0,0)
        #    self.scene.nodewidth(self.id,2)
        else:
            self.scene.nodecolor(self.id, .7, .7, .7)

        while True:  # Trickle algorithm

            if self.version > 0:
                self.send_DIO()

                if DEBUG_MSG: print(f"Trickle. Version: {self.version}, TrickleTime: {self.trickleTime}, Delay: {delay()}, id: {self.id}, tricklecount: {self.trickleCount} ")
                self.trickleCount += 1

            yield self.timeout(self.trickleTime)
            self.trickleTime = pow(self.trickleCount, 1.2) * (
                        delay() + 0.8)  # Time between trickles increase exponentially

    ###################
    def send_DIO(self):
        rplMsg = RPLMessage(type=RPMType.DIO, src=self.id, data=self.rank + 1, sequence=self.sequence_count, version = self.version)
        self.send(wsp.BROADCAST_ADDR, msg=rplMsg)
        self.sequence_count = self.sequence_count + 1

    ###################
    def send_DAO(self, rplMsg=None):
        if rplMsg is None:
            list = [self.id]
            rplMsg = RPLMessage(type=RPMType.DAO, src=self.id, path=list)
        else:
            rplMsg.path.append(self.id)
        self.send(self.prev, msg=rplMsg)

    ###################
    def send_data(self, rplMsg):
        if rplMsg.src is ROOT:
            if self.id is ROOT:  # if root set path to in rplmsg
                rplMsg.path = self.path_to_node(rplMsg.dst)
            self.send(rplMsg.path[self.rank + 1], msg=rplMsg)
        else:
            self.send(self.prev, msg=rplMsg)

    def send_ack(self, msg):
        msg = RPLMessage(type=RPMType.ACK, src=self.id, dst=msg.src, sequence=self.sequence_count)
        print(f'ack > {msg.src} -> {msg.dst} :: {msg.sequence}')
        self.send(self.prev, msg=msg)

    ###################
    def on_receive(self, sender, msg, **kwargs):
        
        if self.batteryCheck() <= 0:
            pass
        elif random.random() < pPackageLoss:  # Packet loss
            pass

        elif msg.type == RPMType.DIO:  # root to nodes
            if self.version < msg.version:
                self.version = msg.version
                self.trickleCount = 1
                #if self.prev is not None: return #We dont understand this line help
                self.rank = msg.data
                self.prev = sender
                self.scene.addlink(sender, self.id, "parent")
                if self.id is not ROOT:
                    self.scene.nodecolor(self.id, 0.7, 0, 0)
                    self.scene.nodewidth(self.id, 2)
                    yield self.timeout(delay())
                    self.send_DIO()  # keep expanding network
                    self.send_DAO()  # send DAO back to root to establish DODAG tree

        elif msg.type == RPMType.DAO:  # nodes to root

            if self.id is ROOT:
                # create tree structure using each returned DAO
                msg.path.append(self.id)
                path = msg.path[::-1]  # reverse list

                print(path)
                print(msg.type, str(msg.data))
                for node in path:
                    string = find_by_attr(self.root, str(node))
                    if not string:
                        Node(str(node), find_by_attr(self.root, str(prevNode)))  # add latest node to root tree
                    prevNode = node

                node = sim.nodes[path[-1]]
                node.scene.nodecolor(node.id, 0, 0, 1)


            else:
                self.next = self.prev
                yield self.timeout(delay())
                self.send_DAO(msg)

        elif msg.type == RPMType.DIS:
            pass

        elif msg.type == RPMType.DATA:
            self.send_ack(msg)
            if self.id is not msg.dst:
                yield self.timeout(delay())
                self.sequence_count = self.sequence_count + 1
                self.send_data(msg)

            else:
                printstr = "node " + str(self.id) + " received: " + msg.data
                cprint(printstr, "OKGREEN")

    

    

    # ----------------- Demo functions ----------------

    def root_print_tree(self):
        if self.id is ROOT:
            for pre, fill, node in RenderTree(self.root):  # print tree
                cprint(pre + node.name, "OKCYAN")

        else:
            cprint("Err: Function only available to root node", "WARNING")

    def path_to_node(self, node):
        """
        Takes node number as either str or int
        returns list of path-nodes from root to node.
        """
        if not type(node) == int: node = int(node)
        string = ""
        if self.id is ROOT:
            if node >= 0 or node <= len(sim.nodes) + 1:
                # find by attr gives weird format back, put each item (ie node jump) into list
                string = str(find_by_attr(self.root, str(node)))[7:].split("/")
                string = [int(re.sub("[^0-9]", "", item)) for item in
                          string]  # removes everything but numbers in the list
                # print(string) # print path from root to node
                return string
            else:
                cprint("Err: Node doesnt exist", "WARNING")

        else:
            cprint("Err: Function only available to root node", "WARNING")
        return string


def user_input():
    while (True):
        inp = input(">>")
        try:
            if inp.lower() == "q":
                exit(0)
            elif inp.isnumeric():
                sim.nodes[ROOT].path_to_node(inp)
                rplMsg = RPLMessage(type=RPMType.DATA, src=ROOT, dst=int(inp), data="hello from root :)")
                sim.nodes[ROOT].send_data(rplMsg)
            elif inp[0].lower() == "n":
                rplMsg = RPLMessage(type=RPMType.DATA, src=inp[1:], dst=ROOT,
                                    data="hello from node {} :)".format(inp[1:]))
                sim.nodes[int(inp[1:])].send_data(rplMsg)
            elif inp.lower() == "tree":
                sim.nodes[ROOT].root_print_tree()
            elif inp.lower() == "repair":
                sim.nodes[ROOT].version += 1
                sim.scene.clearlinks()
                print("Repair sequence INITIATED")
        except:
            cprint("Error with input", "WARNING")


###########################################################

tsize = 800
sim = wsp.Simulator(
    until=1000,
    timescale=5,
    visual=True,
    terrain_size=(tsize, tsize),
    title="IPv6 RPL")

# define a line style for parent links
sim.scene.linestyle("parent", color=(0, .8, 0), arrow="tail", width=2)

#
th = threading.Thread(target=user_input)
th.start()
# place nodes over 100x100 grids
grid = 7
random.seed(42)
for x in range(grid):
    for y in range(grid):
        px = 50 + x * (tsize / 10) * (10 / grid) + random.uniform(-20, 20)
        py = 50 + y * (tsize / 10) * (10 / grid) + random.uniform(-20, 20)
        node = sim.add_node(MyNode, (px, py))

        #node.tx_range = (tsize / 9) * (10 / grid)

        node.logging = True

# start the simulation
sim.run()
