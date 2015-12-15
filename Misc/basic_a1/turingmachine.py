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
"""

from class_turing import TuringMachine

def run_turing(filename):
    """
    @purpose: Starts the turing machine simulation.
    @param: filename - String, specifies the filename of the XML to load from
    @postcondition: Prints the output of the turing machine simulation.
    """
    machine = TuringMachine(filename)
    machine.execute()


if __name__ == "__main__":
    #run_turing("./machines/subtractor-machine.xml")
    #run_turing("./machines/flipper.xml")
    run_turing("./machines/flipperN.xml")
    #run_turing("./machines/simple_adder.xml")
    #run_turing("./machines/simple_counter.xml")
