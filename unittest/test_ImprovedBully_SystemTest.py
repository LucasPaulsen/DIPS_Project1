from random import random
from setuptools import setup
from ImprovedBullyElection import *
import wsnsimpy.wsnsimpy_tk as wsp

import unittest   # The test framework


class Test_ImprovedBully_SystemTest(unittest.TestCase):

    def test_8nodes_starter0(self):
        clearMsgCount()
        setElectionStarter(0)
        sim = wsp.Simulator(
            until=2,
            timescale=1,
            visual=True,
            terrain_size=(SIZE*2,SIZE*2),
            title="Improved Bully Election")
        
        for x in range(4):
            for y in range(2):
                px = 50 + x*200
                py = 50 + y*200
                node = sim.add_node(MyNode, (px,py))
                node.tx_range = 4*SIZE
                node.logging = True

        sim.run()
        self.assertEqual(node.leader,7)
        self.assertTrue(getMsgCount() < (4*2)**2)
        print(f"message count  {getMsgCount()} \n")

        



    def test_8nodes_starter4(self):
        clearMsgCount()
        setElectionStarter(4)
        sim = wsp.Simulator(
            until=2,
            timescale=1,
            visual=True,
            terrain_size=(SIZE*2,SIZE*2),
            title="Improved Bully Election")
        
        for x in range(4):
            for y in range(2):
                px = 50 + x*200
                py = 50 + y*200
                node = sim.add_node(MyNode, (px,py))
                node.tx_range = 4*SIZE
                node.logging = True

        sim.run()
        self.assertEqual(node.leader,7)
        self.assertTrue(getMsgCount() < (4*2)**2)
        print(f"message count  {getMsgCount()} \n")


    def test_8nodes_starter7(self):
        clearMsgCount()
        setElectionStarter(7)
        sim = wsp.Simulator(
            until=2,
            timescale=1,
            visual=True,
            terrain_size=(SIZE*2,SIZE*2),
            title="Improved Bully Election")
        
        for x in range(4):
            for y in range(2):
                px = 50 + x*200
                py = 50 + y*200
                node = sim.add_node(MyNode, (px,py))
                node.tx_range = 4*SIZE
                node.logging = True

        sim.run()

        self.assertEqual(node.leader,7)
        self.assertTrue(getMsgCount() < (4*2)**2)
        print(f"message count  {getMsgCount()} \n")



if __name__ == '__main__':
    unittest.main()


