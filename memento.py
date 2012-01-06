# -*- coding: utf-8 -*-

class Originator():

    class Memento():
        '''  '''
        def __init__(self, stateToSave):
            self.state = stateToSave
            
        def getSavedState(self):
            return self.state
    
    def __init__(self, state=None):
        self.state = state
        
    def set(self, state):
        print "Originator: Setting state to %s" % state
        self.state = int(state)
        
    def saveToMemento(self):
        print "Originator: Saving to Memento."
        return self.Memento(self.state)
        
    def restoreFromMemento(self, m):
        if isinstance(m, self.Memento):
            self.state = m.getSavedState()
            print "Originator: State after restoring from Memento: %s" % self.state
            
            
class Caretaker():
    
    def __init__(self):
        self.savedStates = list()
        
    def addMemento(self, m):
        self.savedStates.append(m)
        
    def getMemento(self, idx):
        return self.savedStates[idx]
        
def main():
    caretaker = Caretaker()
    originator = Originator()

    originator.set("State1")
    originator.set("State2")
    caretaker.addMemento( originator.saveToMemento() )
    originator.set("State3")
    caretaker.addMemento( originator.saveToMemento() )
    originator.set("State4")
 
    originator.restoreFromMemento( caretaker.getMemento(1) )
    
    
if __name__ == '__main__':
    main()