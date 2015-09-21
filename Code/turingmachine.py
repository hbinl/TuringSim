"""
@title Turing Machine Simulator
@author Loh Hao Bin 25461257
@date 01/08/2015
@description A turing machine simulator implementation, written in Python,
            and simulates based on instructions in a XML format.
            
            Works properly for the two input xml provided in Moodle, as well as some
            other sample turing machine (adapted into the XML format) found 
            online, but not all will work (e.g those without transition defined
            for a particular state yet when triggere]\d, will be buggy)

			End
        HHAHAHA

"""

import timeit
from class_turing_string import TuringMachine_String
from class_turing_deque import TuringMachine_Deque
from class_turing_list import TuringMachine_List
import cProfile

def run_turing_list(filename=None):
    """
    @purpose: Starts the turing machine simulation.
    @param: filename - String, specifies the filename of the XML to load from
    @postcondition: Prints the output of the turing machine simulation.
    """
    if filename is None:
        filename = str(input("Filename: "))
    machine = TuringMachine_List(filename)
    machine.execute()

def run_turing_string(filename=None):
    """
    Testing
    @purpose: Starts the turing machine simulation.
    @param: filename - String, specifies the filename of the XML to load from
    @postcondition: Prints the output of the turing machine simulation.
    """
    if filename is None:
        filename = str(input("Filename: "))
    machine = TuringMachine_String(filename)
    machine.execute()

def run_turing_deque(filename=None):
    """
    @purpose: Starts the turing machine simulation.
    @param: filename - String, specifies the filename of the XML to load from
    @postcondition: Prints the output of the turing machine simulation.
    """
    if filename is None:
        filename = str(input("Filename: "))
    machine = TuringMachine_Deque(filename)
    machine.execute()


if __name__ == "__main__":
    #run_turing()

    # fn_list = ["./machines/subtractor-machine.xml","./machines/flipper.xml","./machines/flipperN.xml"]
    #
    # for i in range(len(fn_list)):
    #     run_turing_string(fn_list[i])
    #     run_turing_deque(fn_list[i])
        #run_turing_list(fn_list[i])

    # run_turing("./machines/flipper.xml")
    # run_turing("./machines/flipperN.xml")
    # run_turing("./machines/simple_adder.xml")
    # run_turing("./machines/simple_counter.xml")

    # run_turing("./machines/test1-left-creator.xml")
    # run_turing("./machines/test2-right-creator.xml")
    # run_turing("./machines/test3-right-creator-halt-no.xml")
    # run_turing("./machines/test4-blank-in-middle.xml")

    n = 1500
    # cProfile.run('''timeit.timeit('run_turing_deque("./machines/subtractor-machine.xml")',
    #                     number=10000, setup="from __main__ import run_turing_deque")''')
    print "String ",
    print timeit.timeit('run_turing_string("./machines/subtractor-machine.xml")', number=n,
                        setup="from __main__ import run_turing_string")

    print "Deque ",
    print timeit.timeit('run_turing_deque("./machines/subtractor-machine.xml")',
                        number=n, setup="from __main__ import run_turing_deque")

    print "List ",
    print timeit.timeit('run_turing_list("./machines/subtractor-machine.xml")',
                        number=n, setup="from __main__ import run_turing_list")
