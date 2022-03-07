from ast import NodeTransformer
from ImprovedBullyElection import BullyMsgType, MyNode, MSG_COUNTER, ELECTION_STARTER, SIZE
import wsnsimpy.wsnsimpy_tk as wsp

import unittest   # The test framework



class Test_test_improvedBully(unittest.TestCase):

    def test_2nodes_simple(self):
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
        self.assertEqual(nodeA.bestOK,nodeB.id)


    def test_2nodes_simple1(self):
        ELECTION_STARTER = 1
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
        self.assertEqual(nodeB.bestOK,nodeB.id)


    def test_8nodes_starter0(self):
        ELECTION_STARTER = 0
        sim = wsp.Simulator(
            until=2,
            timescale=1,
            visual=True,
            terrain_size=(SIZE,SIZE),
            title="Improved Bully Election")
        
        for x in range(4):
            for y in range(2):
                px = 50 + x*200
                py = 50 + y*200
                node = sim.add_node(MyNode, (px,py))
                node.tx_range = 2*SIZE
                node.logging = True

        sim.run()
        self.assertEqual(node.id,7)
        self.assertTrue(MSG_COUNTER < (4*2))



    def test_8nodes_starter4(self):
        ELECTION_STARTER = 4
        sim = wsp.Simulator(
            until=2,
            timescale=1,
            visual=True,
            terrain_size=(SIZE,SIZE),
            title="Improved Bully Election")
        
        for x in range(4):
            for y in range(2):
                px = 50 + x*200
                py = 50 + y*200
                node = sim.add_node(MyNode, (px,py))
                node.tx_range = 2*SIZE
                node.logging = True

        sim.run()
        self.assertEqual(node.id,7)
        self.assertTrue(MSG_COUNTER < (4*2))
        






if __name__ == '__main__':
    unittest.main()


