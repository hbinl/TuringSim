"""
@title Turing Machine ADT v2
@author Loh Hao Bin 25461257
@date 01/08/2015
@description A turing machine ADT used to abstract and store data for a TM simulation
            v2: Moved the execution functionality into the class (+1 OOP)
"""

import xml.etree.ElementTree as ET
from collections import deque


class Transition():
    def __init__(self, origin, end, seen, write, move):
        self.origin_node = origin
        self.end_node = end
        self.seen_sym = seen
        self.write_sym = write
        self.move = move

    def get_end_state(self):
        return self.end_node

    def get_write(self):
        return self.write_sym

    def get_move(self):
        return self.move

class State():
    def __init__(self, id):
        self.transitions = {}
        self.id = id
        self.halting = False

    def is_halt(self):
        return self.halting

    def add_transition(self, end, seen, write, move):
        try:
            self.transitions[seen] += Transition(self.id, end, seen, write, move)

        except KeyError:
            self.transitions[seen] = [Transition(self.id, end, seen, write, move)]

    def get_transition_seen(self, seen):
        try:
            return self.transitions[seen]
        except KeyError:
            return []

class TuringMachine_Deque():
    def __init__(self, filename):
        """
        @purpose Initialise the turing machine's variables and status
        :param blankchar: The blank character to use, defaults to #
        :param haltingstate: Specifies the halting state, defaults to H
        """

        # Parse XML
        # loads file using ElementTree library, then preparing to load initial
        # root elements and info (e.g final state, blank chars) from the file
        self.filename = filename
        self.xml_tree = ET.parse(self.filename)
        #print "\nThe filename is {0}".format(self.filename)
        #print(self.xml_tree)
        self.init_state = self.xml_tree.find("initialstate").attrib["name"]
        self.init_tape = self.xml_tree.find("initialtape").text
        self.blank_char = self.xml_tree.find("blank").attrib["char"]
        self.xml_states = self.xml_tree.find("states")
        self.haltingstate = self.xml_tree.find("finalstates").find("finalstate").attrib["name"]
        #print "Blank char: ", self.blank_char

        # Initialising other variables
        self.current_state = None
        self.current_step = 0
        self.halted = False
        # head_position stores the real position of the head as if it were on a
        # real tape, e.g -5 for a head on 5th position from the left of 0th cell,
        # hence, to access the string indices properly, use .get_head_pos_with_offset()
        self.left_offset = 0
        self.head_position = 0
        self.offset = 0

        self.tape = Tape(self.blank_char)
        self.tape.init_tape(self.init_tape)
        self.set_state(self.init_state)

        #self.print_machine()

        self.states = {}
        self.load_states(self.xml_states)


    def load_states(self, state_tree):
        for state in state_tree:
            id = state.attrib["name"]
            self.states[id] = node = State(id)

            for transition in state:
                end = transition.attrib["newstate"]
                seen = transition.attrib["seensym"]
                write = transition.attrib["writesym"]
                move =  transition.attrib["move"]
                node.add_transition(end, seen, write, move)

    def execute(self):
        # Start the simulation
        while not self.is_halted():
            # Increments the step, load current state and current head data
            self.increment_step()
            current_state = self.get_current_state()
            current_read = self.read_current_pos()
            #print(current_state, current_read)

            # Get the current state, and loads the instructions for transitions
            # based on the character read from tape
            transitions = self.states[current_state].get_transition_seen(current_read)
            #print len(transitions)
            for tran in transitions:
                self.set_state(tran.get_end_state())
                self.write_current_pos(tran.get_write())
                move = tran.get_move()
                if move == "L":
                    self.move_left()
                elif move == "R":
                    self.move_right()
                elif move == "N":
                    pass

                # print out the status of the machine
                self.print_machine()

            if len(transitions) == 0:
                # if no transition if defined for a particular symbol in a state, halts
                self.halt()

        # machine halted, check if it is in accepting state
        # if self.get_current_state() == self.haltingstate:
        #     print "halted with answer yes"
        # else:
        #     print "halted with answer no"

    def increment_step(self):
        """
        @purpose Maintains a counter of steps for a TM simulation
        """
        self.current_step += 1

    def move_left(self):
        """
        @purpose Moves the machine head to the left, and extends the tape if necessary
        """
        self.tape.move_left()

    def move_right(self):
        """
        @purpose Moves the machine head to the right, and extends the tape if necessary
        """
        self.tape.move_right()

    def get_current_state(self):
        """
        @purpose Returns the current state of the TM
        """
        return self.current_state

    def set_state(self, state):
        """
        @purpose Allows to set the current state to other states
        :param state: The state to transition to
        """
        self.current_state = state

    def print_machine(self):
        """
        @purpose Prints out the current step, state, and tape of the TM
        """
        print "Steps: ", self.current_step
        print "State: ", self.current_state
        print "Tape: ", self.print_tape()
        print


    def print_tape(self):
        """
        @purpose Returns the whole tape, while highlighting the head position
        """
        self.tape.print_tape()

    def read_current_pos(self):
        """
        @purpose Returns the data on the current position of the head

        """
        return self.tape.read()

    def write_current_pos(self, value):
        """
        @purpose Allows for writing data on the current position of the head
        :param value: The value to be written
        """
        return self.tape.write(value)

    def is_halted(self):
        """
        @purpose Returns whether the machine is currently in a halting state
        :return: True for halted, False for still running
        """
        return self.halted

    def halt(self):
        """
        @purpose halt the machine immediately.
        """
        self.halted = True
        return self.current_state


class Tape():
    def __init__(self, blankchar="b"):
        """
        Tape implementation using collections.deque
        deque allows O(1) access from either side
        To maintain head position, we rotate the deque tape accordingly
        with position 0 always being the head pointed at the tape

        @purpose Initialise the tape. The tape starts off with a blank cell.
        :param blankchar: The blank character representation to use.
        """
        self.tape = deque()
        self.tape.append(blankchar)
        self.blankchar = blankchar

        self.head_pos = 0

    def set_blank_char(self, char):
        self.blankchar = char

    def init_tape(self, tape):
        """
        @purpose Initialise the tape with a custom tape,
        should be used with TuringMachine.set_tape()
        :param tape: The string representation of a initial tape state
        """
        self.tape = deque(tape)

    def print_tape(self):
        """
        @purpose Returns the whole tape
        """
        ind = self.head_pos
        self.tape.rotate(self.head_pos)
        final = "".join(list(self.tape))
        print final[0:ind] + "[" + final[ind] + "]" + final[ind+1:]
        self.tape.rotate(0-self.head_pos)
        return final

    def move_right(self):
        self.tape.rotate(-1)
        self.head_pos += 1
        if self.head_pos >= len(self.tape):
            self.tape.append(self.blankchar)
            self.tape.rotate(1)

    def move_left(self):
        self.head_pos -= 1
        if self.head_pos < 0:
            #self.tape.rotate(-1)
            self.tape.appendleft(self.blankchar)
            self.head_pos = 0
        else:
            self.tape.rotate(1)


    def write(self, value):
        """
        @purpose Writes the value in position pos, on the tape
        :param value: The value to write
        :return:
        """
        self.tape.popleft()
        self.tape.appendleft(value)


    def read(self):
        """
        @purpose returns the data stored on tape at head position
        """
        return self.tape[0]

    def __len__(self):
        """
        @purpose overloading the length operator to get the current visible length of tape
        """
        return len(self.tape)


x = TuringMachine_Deque("flipper.xml")
x.execute()