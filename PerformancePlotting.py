#from ImprovedBullyElection import *
from BullyElection import *
import matplotlib.pyplot as plt
import numpy as np

ELECTION_STARTER = 0
SIZE = 500
MAX_NODES = 20

ns = [] # Number of nodes in each iteration
results = [] # Number of messages sent in each iteration

for n in range(2, MAX_NODES+1):
    ns.append(n)
    clearMsgCount() # Added this to have multiple succeeding simulations

    sim = wsp.Simulator(
            until=1.2,
            timescale=1,
            visual=False, # Not necessary here
            terrain_size=(SIZE,SIZE),
            title="Improved Bully Election")

    for x in range(n):
        node = sim.add_node(MyNode, (x,x)) # Position still has to vary, hence (x,x)
        node.tx_range = 2*SIZE
        node.logging = True
    sim.run()
    results.append(getMsgCount())

plt.scatter(ns, results)
plt.title("Improved bully algorithm")
plt.xlabel("Number of nodes")
plt.ylabel("Number of messages")
plt.xticks(np.linspace(2,20,10))
plt.yticks(np.linspace(0,60,7))
plt.show()
