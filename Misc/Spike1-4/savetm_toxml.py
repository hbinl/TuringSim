__author__ = 'varshineeservansingh'

"""
LIBRARIES IMPORTED TO ENABLE THE CODE TO WORK
"""
from xml import etree
from xml.etree import ElementTree
from xml.etree.ElementTree import *
from xml.etree.ElementTree import SubElement
import os


def menu():
    """
    MENU DISPLAYING LIST OF OPTIONS

    @author: Varshinee Devi Servansingh
    @since: 26th of August 2015
    @modified: 1st of September 2015
    @param:  None
    @pre: main() function should be running
    @post: function will either call create_newTM or update_tm, or quit
    :return: None
    @complexity: depends on the functions being called ~

    """
    while True:
        print("Please select an option below:\n1. Save a new turing machine to xml")
        print("2. Update existing xml file with turing machine\n3. Quit")
        try:
            prompt = int(input("Please enter an option number between 1-3 "))   # prompt user for selection
        except ValueError:          # catch alphabets
            prompt = int(input("Please enter an option number between 1-3 "))
        except SyntaxError:         # catch symbols
            prompt = int(input("Please enter an option number between 1-3 "))

            # while not quit
        if prompt == 1:
            tree = create_newTM()  # saving a brand new turing machine
            save_tm(tree)
        elif prompt == 2:  # updating an existing xml file
            update_tm()
        else:
            try:
                prompt = int(input("Please enter an option number between 1-3"))
            except ValueError:
                prompt = int(input("Please enter an option number between 1-3"))
            except SyntaxError:
                prompt = int(input("Please enter an option number between 1-3"))
        if prompt == 3:
            print("Thank you for using this program. Have a nice day!")
            break

def create_newTM():

    """
    @author: Varshinee Devi Servansingh
    @since: 26th of August 2015
    @modified: 1st of September 2015
    @param:  None
    @pre: user chose to create new turing machine
    @post: function will write all new changes to variable tree and return it
    :return: tree
    @complexity: O(1), since all steps are executed unconditionally, once.
    """

    root = Element("turingmachine")  #

    SubElement(root, "alphabet")  #
    SubElement(root, "initialtape")  #
    SubElement(root, "blank", char="")  # creating the turing machine
    SubElement(root, "initialstate")  #

    finalstates = SubElement(root, "finalstates")  #
    SubElement(finalstates, "finalstate")  #

    SubElement(root, "states")  #

    tree = ElementTree(root)

    return tree


def update_tm():

    """
    @author: Varshinee Devi Servansingh
    @since: 26th of August 2015
    @modified: 1st of September 2015
    @param:  None
    @pre: user chose to update a new file
    @post: function will update the original file and return to main function
    :return: None
    @complexity: O(1)
    """
    original_file = str(raw_input("Please enter the existing file that you wish to update "))
    or_file = open(original_file, 'r')  # calling original file
    tm_data = or_file.readlines()

    tree = create_newTM()
    tree.write("temp_file.xml")

    # tree_str = str(tree)  # convert original file to string before copying
    # with open("temp_file.xml", "w") as f:  # save new additions to temporary file and read from it
    #     f.write(tree_str)

    new_file = open("temp_file.xml", 'r')
    more_data = new_file.readlines()
    print more_data

    output_file = original_file

    with open(output_file, "w") as f:  # update original file with new additions
        f.writelines(tm_data)
        f.writelines(more_data)

    os.remove("temp_file.xml")  # delete temporary file


def save_tm(tree):

    """
    @author: Varshinee Devi Servansingh
    @since: 26th of August 2015
    @modified: 1st of September 2015
    @param:  tree
    @pre: user has already created the turing machine to be saved
    @post: a new xml file will be created, then back to main function
    :return: None
    @complexity: O(1)
    """
    output_file = str(raw_input("Please enter a file name to save your turing machine "))
    tree.write(output_file)


def main():
    menu()


if __name__ == '__main__':
    main()