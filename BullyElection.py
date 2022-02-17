class MessageBroker:
    def __init__(self):
        self.msgCount = 0
    def reset(self):
        self.msgCount = 0
    def msg(self, sndr, rcvr, text):
        self.msgCount += 1
        print(f"{self.msgCount}: P{sndr.ID}->P{rcvr.ID} - " + text)

class Process:
    def __init__(self, ID, alive, msgBroker):
        self.ID = ID
        self.alive = alive # whether the proces is alive
        self.otherNodes = [] # list of all other processes in the system
        self.bullied = False # indicates if the process has been bullied/overruled
        self.elecPending = False # if the proces has just OK'd an election msg
        self.coordPending = False # if the process has not been bullied and is about to be the coordinator
        self.coordWait = 2 # Cycles to pass before announcing itself as coordinator
        self.msgBroker = msgBroker # Reference to global message broker
    
    def setOtherProcs(self, procs):
        for p in procs:
            if (p != self):
                self.otherNodes.append(p)

    def tick(self):
        if self.elecPending:
            self.sendElection()
        if self.coordPending:
            if(self.coordWait > 0):
                self.coordWait -= 1
            elif (self.coordWait == 0):
                for p in self.otherNodes:                    
                    self.msgBroker.msg(self, p, "Coordinator")
                self.coordPending = False
                self.coordWait = 3
            
    def sendElection(self):
        self.elecPending = False
        self.bullied = False
        for p in self.otherNodes:
            if(p.ID > self.ID):
                self.msgBroker.msg(self, p, "Election")
                p.receiveElection(self)
        if(self.bullied == False):
            self.coordPending = True
                
    def receiveElection(self, p):
        if(self.alive and self.ID > p.ID):
            self.elecPending = True
            self.msgBroker.msg(self, p, "OK")
            p.receiveOK(self)
            
    def receiveOK(self, p): # 
        self.bullied = True


def Simulation(nProc, startProc, maxIter):
    # nProc = number of processes to include
    # startProc = the process starting the election  
    msgBroker = MessageBroker()
    procs = []
    for i in range(nProc):
        Px = Process(i+1, True, msgBroker)
        procs.append(Px)
    
    for p in procs:
        p.setOtherProcs(procs)
        
    procs[startProc].sendElection()
    
    for i in range(maxIter):
        for p in procs:
            p.tick()
        
   
Simulation(60, 0, 100) # Run simulation
        