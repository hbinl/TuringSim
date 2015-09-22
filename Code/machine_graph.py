
# SpikeMachine, a simple class used to keep track of the current Turing Machine in memory

class SpikeMachine():
    def __init__(self):
        self.states = {}
        self.transitions = {}

    def add_state(self, id, reference):
        self.states[id] = reference

    def delete_state(self, id):
        del self.states[id]

    def add_transition(self, origin, destination):
        #TODO: Transitions not needed for A3
        pass

    def delete_transition(self, origin, destination):
        #TODO: Transitions not needed for A3
        pass

    def modify_state(self,original_id,new_id):
        pass


