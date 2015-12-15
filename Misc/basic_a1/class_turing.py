"""
@title Turing Machine ADT v2
@author Loh Hao Bin 25461257
@date 01/08/2015
@description A turing machine ADT used to abstract and store data for a TM simulation
            v2: Moved the execution functionality into the class (+1 OOP)
"""

import xml.etree.ElementTree as ET

class TuringMachine():
    def __init__(self, filename):
        """
        @purpose Initialise the turing machine's variables and status
        :param blankchar: The blank character to use, defaults to #
        :param haltingstate: Specifies the halting state, defaults to H
        """
        # loads file using ElementTree library, then preparing to load initial
        # root elements and info (e.g final state, blank chars) from the file
        self.filename = filename
        self.xml_tree = ET.parse(filename)
        print "The filename is {0}".format(filename)

        self.init_state = self.xml_tree.find("initialstate").attrib["name"]
        self.init_tape = self.xml_tree.find("initialtape").text
        self.blank_char = self.xml_tree.find("blank").attrib["char"]
        self.xml_states = self.xml_tree.find("states")
        self.haltingstate = self.xml_tree.find("finalstates").find("finalstate").attrib["name"]
        print "Blank char: ", self.blank_char

        #self.haltingstate = self.halting_state
        self.tape = Tape(self.blank_char)
        self.current_state = None
        self.current_step = 0
        self.halted = False
        self.left_offset = 0
        self.head_position = 0
        # head_position stores the real position of the head as if it were on a
        # real tape, e.g -5 for a head on 5th position from the left of 0th cell,
        # hence, to access the string indices properly, use .get_head_pos_with_offset()

        self.set_tape(self.init_tape)
        self.set_state(self.init_state)
        self.print_machine()

    def execute(self):
        # Start the simulation
        while not self.is_halted():
            # Increments the step, load current state and current head data
            self.increment_step()
            current_state = self.get_state()
            current_read = self.read_current_pos()

            # Get the current state, and loads the instructions for transitions
            # based on the character read from tape
            in_state = self.get_child_with_attribute_value(self.xml_states, "name", current_state)[0]
            in_state_read = self.get_child_with_attribute_value(in_state, "seensym", current_read)

            # if there exists a next transition for the state/character
            if len(in_state_read) > 0:
                # Write symbol, and move to next state
                actions = in_state_read[0]
                self.write_current_pos(actions.attrib["writesym"])
                self.set_state(actions.attrib["newstate"])

                # move head accordingly
                if actions.attrib["move"] == "L":
                    self.move_left()
                elif actions.attrib["move"] == "R":
                    self.move_right()
                elif actions.attrib["move"] == "N":
                    pass

                # print out the status of the machine
                self.print_machine()

            else:
                # if no transition if defined for a particular symbol in a state, halts
                self.halt()

        # machine halted, check if it is in accepting state
        if self.get_state() == self.haltingstate:
            print "halted with answer yes"
        else:
            print "halted with answer no"

    def get_child_with_attribute_value(self, tree, attribute, value):
        """
        @purpose: Get all the children, which matches the attribute/value combo specified,
        of the tree/subtree.

        :param tree: The tree in which to search for a child
        :param attribute: The attribute name to search for
        :param value: The value of the attribute to match
        :return: Returns the Element objects based on the attribute/value findings
        """

        # The .findall() and .find() methods support XPath expressions
        # . Current node
        # / substructure
        # * all children
        # [@attribute=value] selects all matching attributes with value

        xpath_expression = "./*[@" + attribute + "='" + value + "']"
        return tree.findall(xpath_expression)

    def set_head_pos(self,head_pos):
        """
        @purpose Allows to set the position of the head to arbitrary positions
        specified by head_pos

        :param head_pos: Custom position to set the head to
        """
        if head_pos >= len(self.tape):
            max_position =  len(self.tape)-1
            offset = head_pos - max_position
            self.head_position = max_position
            for _ in range(offset):
                self.move_right()
        elif head_pos < 0:
            offset = 0 - head_pos
            self.head_position = 0
            for _ in range(offset):
                self.move_left()


    def increment_step(self):
        """
        @purpose Maintains a counter of steps for a TM simulation
        """
        self.current_step += 1

    def move_left(self):
        """
        @purpose Moves the machine head to the left, and extends the tape if necessary
        """
        self.head_position -= 1
        if self.head_position < 0:
            self.tape.extend_left()
            self.left_offset += 1

    def move_right(self):
        """
        @purpose Moves the machine head to the right, and extends the tape if necessary
        """
        self.head_position += 1
        if self.get_head_pos_with_offset() >= len(self.tape):
            self.tape.extend_right()

    def get_state(self):
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

    def set_tape(self, initial_tape):
        """
        @purpose Initialising the tape of the TM with a supplied tape
        :param initial_tape: The initial set of data to set on tape, which is a string of
                            characters
        :return:
        """
        self.tape.init_tape(initial_tape)

    def get_tape(self):
        """
        @purpose Returns the tape object
        """
        return self.tape

    def get_head_pos_with_offset(self):
        """
        @purpose Returns the true index position of the head
        Because if the tape has been extended to the left, there would be a Left_offset
        which will affect string array indices.
        """
        return self.head_position + self.left_offset

    def print_tape(self):
        """
        @purpose Returns the whole tape, while highlighting the head position
        """
        pos = self.get_head_pos_with_offset()
        tape = self.tape.read_tape()
        return tape[0:pos] + "[" + tape[pos] + "]" + tape[pos+1:]

    def read_current_pos(self):
        """
        @purpose Returns the data on the current position of the head

        """
        return self.tape.read(self.get_head_pos_with_offset())

    def write_current_pos(self, value):
        """
        @purpose Allows for writing data on the current position of the head
        :param value: The value to be written
        """
        return self.tape.write(self.get_head_pos_with_offset(), value)

    def is_halted(self):
        """
        @purpose Returns whether the machine is currently in a halting state
        :return: True for halted, False for still running
        """
        if self.current_state == self.haltingstate:
            self.halted = True
            return True
        else:
            return False

    def halt(self):
        """
        @purpose halt the machine immediately.
        """
        self.halted = True
        return self.current_state


class Tape():
    def __init__(self, blankchar="#"):
        """
        @purpose Initialise the tape. The tape starts off with a blank cell.
        :param blankchar: The blank character representation to use.
        """
        self.tape = blankchar
        self.blankchar = blankchar

    def init_tape(self, tape):
        """
        @purpose Initialise the tape with a custom tape,
        should be used with TuringMachine.set_tape()
        :param tape: The string representation of a initial tape state
        """
        self.tape = tape

    def write(self, pos, value):
        """
        @purpose Writes the value in position pos, on the tape
        :param pos: The index to be overwritten with the value
        :param value: The value to write
        :return:
        """
        self.tape = self.tape[0:pos] + value + self.tape[pos+1:]
        return self.tape

    def read_tape(self):
        """
        @purpose Returns the whole tape
        """
        return self.tape

    def read(self, pos):
        """
        @purpose returns the data stored on tape at position pos
        :param pos: The index to access
        """
        return self.tape[pos]

    def __len__(self):
        """
        @purpose overloading the length operator to get the current visible length of tape
        """
        return len(self.tape)

    def extend_left(self):
        """
        @purpose Extends the left side of the tape infinitely with blank spaces
        """
        self.tape = self.blankchar + self.tape
        return self.tape

    def extend_right(self):
        """
        @purpose Extends the right side of the tape infinitely with blank spaces
        """
        self.tape = self.tape + self.blankchar
        return self.tape
