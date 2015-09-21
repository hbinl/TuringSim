"""
@title FIT3140 Assignment 3 Spikes All in One Version
@description Spike test, contains Spike 1, 2, 3 and 4

            #######################################################
            To look for codes related to a particular spike,
            just find "Spike1", "#Spike2", "#Spike3" or "#Spike4"
            #######################################################

@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 1/9/2015
"""

# Kivy Dependencies
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.graphics.transformation import Matrix
from kivy.animation import Animation

# Python Libraries
import os
import xml.etree.ElementTree as ET

# Team Spike Files
from spike_ui_lib import *   #Spike2
from spike_dialog import *
from savetm_toxml import *   #Spike1
from spike_graph import SpikeMachine


class Container(Widget):
    """
    @purpose Main container class, containing various general UI handlers
    """
    def __init__(self, **kwargs):
        # Constructor
        super(Container, self).__init__(**kwargs)

        # Initialise SpikeMachine class used to keep track of states
        self.machine = SpikeMachine()
        self.xml_tree = None

        #Spike3
        # Initialising edit mode flag
        self.edit_mode = False

        #Spike4
        # Initialise variables for use with Scatterlayout, setting maximum/min scaling,
        # Disabling single finger move canvas, disabling rotation
        self.zoomed = False
        Window.clearcolor = (0.7, 0.7, 0.7, 1)
        self.ids.layout_states.scale_max = 1.5
        self.ids.layout_states.scale_min = 0.1
        self.ids.layout_states.translation_touches = 2
        self.ids.layout_states.do_rotation = False


    #Spike1
    def savexml_handler(self, text):
        # Method used to test Spike 1, which is to test ability to save XML files

        self._popup = Popup(title="Spike 1 Save XML",
                            content=Spike1Message(),
                            size_hint=(0.9,0.3))
        self._popup.open()



    #Spike3
    def save_handler(self, text):
        #Handler for Spike3 save button, saves the customised Turing machine to xml

        # Check if currently there is a xml file loaded
        # if there is currently a xml loaded, update the xml file in 1.xml
        # else, create a new turing machine xml file in 1.xml

        # TO-DO: User input the name of the file. For now it's all 1.xml

        if self.xml_tree is not None:
            # If currently there is a xml loaded

            # get the current xml tree, and remove all the states
            xml_tree = self.xml_tree
            xml_states = xml_tree.find("states")
            for state in xml_states.findall("state"):
                xml_states.remove(state)
            print self.machine.states

            # add in the current states in the memory
            for key,value in self.machine.states.iteritems():
                print key, value.id
                SubElement(xml_states, "state", {"name":value.id})

            # save file!
            xml_tree.write("1.xml")
            self._popup = Popup(title="Spike 3 modifications saved in 1.xml",
                            content=None,
                            size_hint=(0.9,0.3))
            self._popup.open()

        else:
            # if no xml file loaded, create new
            tree = create_newTM()
            tree.write("1.xml")
            xml_states = tree.find("states")

            for state in xml_states.findall("state"):
                xml_states.remove(state)

            # add in the current states in memory
            for key,value in self.machine.states.iteritems():
                print key, value.id
                SubElement(xml_states, "state", {"name":value.id})
            tree.write("1.xml")



    #Spike3
    def edit_handler(self, button):
        # Handles the edit button click

        # Condition checks if we are currently in edit mode

        if button.text == "Done":
            # if in edit mode, clicking done will clean up and exit edit mode
            button.text ="Spike3 Edit"
            self.children[0].canvas.clear()
            self.remove_widget(self.children[0])
            self.edit_mode = False
        else:
            # We are in edit mode
            button.text = "Done"
            self.edit_mode = True

            # Shows the customisation toolbar
            bl = UIObj_Edit()
            self.add_widget(bl)
            anim = Animation(x=0, y=0, duration=0.2)
            anim.start(bl)

            # Adds template objects to customisation toolbar
            bl.add_widget(UIObj_State_Template(id="State",
                                               x = 600,
                                               y = 10,
                                               size=(100,100)))
            bl.add_widget(UIObj_State_Halting_Template(id="Halt",
                                                       x=760,
                                                       y=10,
                                                       size =(100,100)))



    #Spike4
    def zoomplus_handler(self):
        # Handles the zoom + button, and scales the ScatterLayout by 1.25x
        # self.zoomed flag ensures the + and - button can only be clicked once
        # without clicking the other

        if self.zoomed is False:
            self.zoomed = True
            mat = Matrix().scale(1.25, 1.25, 1.25)
            self.ids.layout_states.apply_transform(mat)

    #Spike4
    def zoomminus_handler(self):
        # Handles the zoom - button, and scales the ScatterLayout by 0.8x
        # self.zoomed flag ensures the + and - button can only be clicked once
        # without clicking the other

        if self.zoomed is True:
            mat = Matrix().scale(0.8, 0.8, 0.8)
            self.ids.layout_states.apply_transform(mat)
            self.zoomed = False



    def load_handler(self, text):
        # Purpose: Shows a file browser dialog for user to pick an XML file
        self._popup = Popup(title="Load a Turing Machine XML File",
                            content=BrowseFileChooserWindow(),
                            size_hint=(0.85, 0.85))

        # Assign handler on dismiss
        self._popup.bind(on_dismiss=self.after_load_handler)

        # Reveal dialog
        self._popup.open()

    def after_load_handler(self, obj):
        # Purpose: To handle loading file and data from XML file

        # Check if the user has selected a file to load from
        if obj.content.path is not None:
            # Initialising UI variables, clearing canvas and setting the stage
            self.zoomminus_handler()
            self.edit_mode = False
            board = self.ids.layout_states
            board.pos = (0,0)
            board.clear_widgets()

            # Initialising appearance variables for States
            i = 0
            win_x, win_y = Window.size
            start = 150
            state_size = 100
            padding = 80
            y_hint = 0.2
            state_size = 100

            # reading from XML file
            xml_tree = ET.parse(obj.content.path)
            self.xml_tree = xml_tree
            xml_states = xml_tree.find("states")

            # Start looping through the XML file
            for child in xml_states:
                # Calculate position for the state to appear in
                x_pos = start+(i*(state_size+padding))
                if x_pos > Window.size[0]:
                    i = 0
                    x_pos = start+(i*(state_size+padding))
                    y_hint += 0.1
                y_pos = win_y*y_hint

                # If halt, create halt object, else create ordinary state object
                if child.attrib["name"] == "halt":
                    state = UIObj_State_Halting(id=str(child.attrib["name"]),
                                                x = x_pos,
                                                y = y_pos,
                                                size=(state_size,state_size))
                else:
                    state = UIObj_State(id=str(child.attrib["name"]),
                                        x = x_pos,
                                        y = y_pos,
                                        size=(state_size,state_size))

                # Add the states to the canvas, and keep track of states in memory
                self.machine.add_state(str(child.attrib["name"]),state)
                board.add_widget(state)
                i += 1

                # # TODO_FUTURE TRANSITION STUFFS
                # transition = UIObj_Transition(tid=str(child.attrib["name"]),
                #                               origin_x=x_pos+(state_size/2),origin_y=y_pos+(state_size/2),
                #                               end_x=x_pos*2, end_y=y_pos*2,
                #                               width=transition_width,
                #                               curve_factor=25,
                #                               is_self_state=False)
                # board.add_widget(transition)
                # print self.machine.states


# KIVY HANDLING STUFF BELOW
class Spike2App(App):
    def build(self):
        return Container()

if __name__=="__main__":
    Spike2App().run()