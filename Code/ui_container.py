__author__ = 'HaoBin'

# Kivy Dependencies
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
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
from kivy.clock import Clock

# Python Libraries
import os
import xml.etree.ElementTree as ET

# Team Spike Files
from ui_lib import *   #Spike2
from ui_dialog import *
from savetm_toxml import *   #Spike1
from machine_graph import SpikeMachine


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
        self._popup = None

        #Spike4
        # Initialise variables for use with Scatterlayout, setting maximum/min scaling,
        # Disabling single finger move canvas, disabling rotation
        self.zoomed = False
        Window.clearcolor = (0.7, 0.7, 0.7, 1)
        self.ids.layout_states.scale_max = 1.0
        self.ids.layout_states.scale_min = 0.32768
        self.ids.layout_states.translation_touches = 2
        self.ids.layout_states.do_rotation = False
        self.zoom_counter = 0

        self.home_screen(self)

        self.edit_mode_selected_state = None

    def home_screen(self, obj):
        if self._popup is not None:
            self._popup.dismiss()


        self.home_popup = Popup(title="Turing Machine Simulator",
                            content=HomeScreenWindow(),
                            size_hint=(1, 1),
                            auto_dismiss=False)

        load_button = self.home_popup.content.ids.home_load
        new_dtm_button = self.home_popup.content.ids.home_new_dtm
        # new_ndtm_button = self.home_popup.content.ids.home_new_ndtm

        load_button.bind(on_release=self.load_handler)
        # new_dtm_button.bind(on_release=self.home_popup.dismiss)

        print "home"
        # # Assign handler on dismiss
        # self.home_popup.bind(on_dismiss=self.after_load_handler)

        # Reveal dialog
        Clock.schedule_once(self.home_popup.open, 0.5)
        #self.home_popup.open()


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
        if self.edit_mode is True:
            self.edit_mode_controller(False)
        else:
            self.edit_mode_controller(True)



    def edit_mode_controller(self, flag):
        button = self.ids.edit_button

        if flag is False:

            if button is not None:
                button.text = "Edit"

            self.children[0].canvas.clear()
            self.remove_widget(self.children[0])
            self.edit_mode = False
            if self.edit_mode_selected_state is not None:
                print self.edit_mode_selected_state.id
                print self.edit_mode_selected_state.menu
                print self.edit_mode_selected_state.menu.parent
                self.edit_mode_selected_state.menu.parent.remove_widget(self.edit_mode_selected_state.menu)
            self.edit_mode_selected_state = None
        else:
            if button is not None:
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



    def zoom_handler(self):
        if self.zoom_counter < 5:
            self.zoom_counter += 1
            mat = Matrix().scale(0.8,0.8,0.8)
            self.ids.layout_states.apply_transform(mat)
        else:
            self.zoom_reset()

    def zoom_reset(self):
        self.zoom_counter = 0
        factor = 1/self.ids.layout_states.scale
        mat = Matrix().scale(factor, factor, factor)
        self.ids.layout_states.apply_transform(mat)

    def close_handler(self):
        content = BoxLayout(orientation="vertical")

        content.add_widget(Label(text="Are you sure you want to close the TM?"))

        content_box = BoxLayout(orientation="horizontal")

        ok_button = Button(text="Yes")
        content_box.add_widget(ok_button)

        cancel_button = Button(text="No")
        content_box.add_widget(cancel_button)

        content.add_widget(content_box)

        self._popup = Popup(title="Return to Home",
                            content=content,
                            size_hint=(0.6, 0.3),
                            auto_dismiss=False)

        ok_button.bind(on_release=self.home_screen)
        cancel_button.bind(on_release=self._popup.dismiss)

        if self.edit_mode is True:
            self.edit_mode_controller(False)

        # Reveal dialog
        self._popup.open()


    def load_handler(self, text):
        # Purpose: Shows a file browser dialog for user to pick an XML file

        self._popup = Popup(title="Load a Turing Machine XML File",
                            content=BrowseFileChooserWindow(),
                            size_hint=(0.85, 0.85))

        # Assign handler on dismiss
        self._popup.bind(on_dismiss=self.after_load_handler)
        self._popup.content.ids.cancel_button.bind(on_release=self.home_screen)

        # Reveal dialog
        self._popup.open()

    def after_load_handler(self, obj):
        # Purpose: To handle loading file and data from XML file

        # Check if the user has selected a file to load from
        if obj.content.path is not None:
            self.home_popup.dismiss()

            # Initialising UI variables, clearing canvas and setting the stage
            self.zoom_reset()
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

