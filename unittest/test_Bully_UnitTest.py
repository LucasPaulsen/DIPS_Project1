from random import random
from setuptools import setup
from BullyElection import *
import wsnsimpy.wsnsimpy_tk as wsp

import unittest   # The test framework


class Test_Bully_UnitTest(unittest.TestCase):

    def test_2nodes_start0(self):
        clearMsgCount()
        setElectionStarter(0)
        sim = wsp.Simulator(
            until=2,
            timescale=1,
            visual=True,
            terrain_size=(SIZE,SIZE),
            title="Improved Bully Election")
        
        nodeA = sim.add_node(MyNode, (100,100))
        nodeA.tx_range = 2*SIZE
        nodeA.logging = True

        nodeB = sim.add_node(MyNode, (130,130))
        nodeB.tx_range = 2*SIZE
        nodeB.logging = True

        sim.run()
        self.assertEqual(nodeA.leader,nodeB.id)
        print(f"message count  {getMsgCount()} \n")


    def test_2nodes_start1(self):
        clearMsgCount()
        setElectionStarter(1)
        sim = wsp.Simulator(
            until=2,
            timescale=1,
            visual=True,
            terrain_size=(SIZE,SIZE),
            title="Improved Bully Election")
        
        nodeA = sim.add_node(MyNode, (100,100))
        nodeA.tx_range = 2*SIZE
        nodeA.logging = True

        nodeB = sim.add_node(MyNode, (130,130))
        nodeB.tx_range = 2*SIZE
        nodeB.logging = True

        sim.run()
        self.assertEqual(nodeB.leader,nodeB.id)
        print(f"message count  {getMsgCount()} \n")



if __name__ == '__main__':
    unittest.main()


