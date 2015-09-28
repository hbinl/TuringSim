"""
@title Turing Machine ADT v2
@author Loh Hao Bin 25461257
@date 01/08/2015
@description A turing machine ADT used to abstract and store data for a TM simulation
            v2: Moved the execution functionality into the class (+1 OOP)
"""

import xml.etree.ElementTree as ET
from collections import deque


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

    def get_head_pos(self):
        """
        @purpose Return the tape head position
        """
        return self.head_pos

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
        """
        @purpose Moves the tape head to the right by 1
        """
        self.tape.rotate(-1)
        self.head_pos += 1
        if self.head_pos >= len(self.tape):
            self.tape.append(self.blankchar)
            self.tape.rotate(1)

    def move_left(self):
        """
        @purpose Moves the tape head to the left by 1
        """
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
        @purpose Returns the data stored on tape at head position
        """
        return self.tape[0]

    def __len__(self):
        """
        @purpose Overloading the length operator to get the current visible length of tape
        """
        return len(self.tape)