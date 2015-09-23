"""
@title FIT3140 Assignment 5
@description Sprint 1
@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 1/9/2015
"""

# Kivy Dependencies
from kivy.uix.button import Button
from kivy.graphics.transformation import Matrix
from kivy.clock import Clock


from ui_dialog import *
from ui_edit import *
from savetm_toxml import *
#from machine_graph import Machine



class Container(Widget):

    class Machine():
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


    """
    @purpose Main container class, containing various general UI handlers
    """
    def __init__(self, **kwargs):
        # Constructor
        super(Container, self).__init__(**kwargs)

        # Initialise SpikeMachine class used to keep track of states
        self.machine = self.Machine()
        self.xml_tree = None

        # Initialising edit mode flag
        self.edit_mode = False
        self.edit_mode_selected_state = None
        self._popup = None

        # Initialise variables for use with Scatterlayout, setting maximum/min scaling,
        # Disabling single finger move canvas, disabling rotation
        Window.clearcolor = (0.7, 0.7, 0.7, 1)
        self.ids.layout_states.scale_max = 3.05175
        self.ids.layout_states.scale_min = 0.32768
        self.ids.layout_states.translation_touches = 2
        self.ids.layout_states.do_rotation = False
        self.zoom_counter = 0

        self.home_screen(self)



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
        new_dtm_button.bind(on_release=self.create_new_handler)

        print "home"

        # Reveal dialog
        Clock.schedule_once(self.home_popup.open, 0.5)


    def create_new_handler(self, obj):
        self.reset_container()
        self.edit_mode_controller(True)
        self.home_popup.dismiss()

    def load_handler(self, obj):
        # Purpose: Shows a file browser dialog for user to pick an XML file

        self._popup = Popup(title="Load a Turing Machine XML File",
                            content=BrowseFileChooserWindow(),
                            size_hint=(0.85, 0.85))

        # Assign handler on dismiss
        self._popup.bind(on_dismiss=self.after_load_handler)
        self._popup.content.ids.cancel_button.bind(on_release=self._popup.dismiss)

        # Reveal dialog
        self._popup.open()

    def reset_container(self):
        self.zoom_reset()
        self.ids.layout_states.pos = (0,0)
        self.ids.layout_states.clear_widgets()

    def after_load_handler(self, obj):
        # Purpose: To handle loading file and data from XML file

        # Check if the user has selected a file to load from
        if obj.content.path is not None:
            self.home_popup.dismiss()

            # Initialising UI variables, clearing canvas and setting the stage
            self.reset_container()
            board = self.ids.layout_states

            # Initialising appearance variables for States
            i = 0
            win_x, win_y = Window.size
            start = 100
            state_size = 100
            padding = 80
            y_hint = 0.1
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
                #                               start=1
                #                               )
                # board.add_widget(transition)
                # print self.machine.states

    def create_state(self, name, halting):

        # Initialising appearance variables for States
        i = 0
        win_x, win_y = Window.size
        start = 100
        state_size = 100
        padding = 80
        y_hint = 0.1
        state_size = 100

        # reading from XML file



        board = self.ids.layout_states
        if halting is True:
            pass
        else:
            state = UIObj_State(id=str(name),
                                                x = 150,
                                                y = 150,
                                                size=(state_size,state_size))

            board.add_widget(state)

    def close_handler(self):
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Are you sure you want to close the TM?"))
        content_box = BoxLayout(orientation="horizontal")

        ok_button = Button(text="Yes")
        cancel_button = Button(text="No")
        content_box.add_widget(ok_button)
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

            # # Adds template objects to customisation toolbar
            # bl.add_widget(UIObj_State_Template(id="State",
            #                                    x = 600,
            #                                    y = 10,
            #                                    size=(100,100)))
            # bl.add_widget(UIObj_State_Halting_Template(id="Halt",
            #                                            x=760,
            #                                            y=10,
            #                                            size =(100,100)))



    def zoom_handler(self, text):
        if text == "Zoom In":
            if self.ids.layout_states.scale < 3.05175:
                mat = Matrix().scale(1.25,1.25,1.25)
                self.ids.layout_states.apply_transform(mat)
        elif text == "Zoom Out":
            if self.ids.layout_states.scale > 0.32768:
                mat = Matrix().scale(0.8,0.8,0.8)
                self.ids.layout_states.apply_transform(mat)


    def zoom_reset(self):
        self.ids.layout_states.pos = [0,0]
        self.zoom_counter = 0
        factor = 1/self.ids.layout_states.scale
        mat = Matrix().scale(factor, factor, factor)
        self.ids.layout_states.apply_transform(mat)


    def about_handler(self):
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="TuringSim v0.1, \nby Loh Hao Bin, Ashley Ong Yik Mun & Varshinee Servansingh\nFIT3140 Advanced Programming, Semester 2, 2015"))

        self._popup = Popup(title="About TuringSim",
                            content=content,
                            size_hint=(0.6, 0.3))

        self._popup.open()




