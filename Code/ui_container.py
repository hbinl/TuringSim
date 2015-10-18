"""
@title FIT3140 Assignment 5
@description Sprint 2
@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 17/10/2015
"""

# Kivy Dependencies
from kivy.uix.button import Button
from kivy.graphics.transformation import Matrix
from kivy.clock import Clock
import random

from ui_dialog import *
from ui_edit import *
#from savetm_toxml import *
#from machine_graph import Machine
from tape import Tape
from xml.etree.ElementTree import *


from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

class Container(Widget):

    class Machine():
        def __init__(self,blankchar="b"):
            """
            @purpose Initialise the Machine class used to keep track of states. The tape starts off with a blank cell.
            :param blankchar: The blank character representation to use.
            """
            self.states = {}
            self.transitions = {}
            self.starting = None
            self.tape = Tape(blankchar)
            self.halting_states = {}
            self.blankchar = blankchar

            self.current_step = 0
            self.current_state = self.starting
            self.current_read = None
            self.current_transition = None
            self.halted = False

        def get_num_states(self):
            # Returns the number of states currently in the machine
            return len(self.states)

        def is_halted(self):
            """
            @purpose Returns halted in boolean
            """
            return self.halted

        def halt(self):
            """
            @purpose Sets halt to True
            """
            self.halted = True

        def set_tape(self, tape):
            """
            @purpose Sets the tape to the initial tape
            :param tape: Takes in the initial tape
            :return:
            """
            self.tape.init_tape(tape)

        def set_blank_char(self, char):
            """
            @purpose Sets the blankchar to char
            :param char: Takes in character 'b'
            :return:
            """
            self.blankchar = char

        def get_tape(self):
            """
            @purpose Returns the whole tape
            """
            return self.tape.print_tape()

        def get_current_tape_head_pos(self):
            """
            @purpose Returns the current tape head position
            """
            return self.tape.get_head_pos()

        def set_starting(self, id):
            """
            @purpose Set the current state to the staring state
            :param id: ID of the state
            :return:
            """
            try:
                self.starting = self.states[id]
                if self.current_step == 0:
                    self.current_state = self.starting

            except KeyError:
                raise Exception("State does not exist.")

        def get_starting_state(self):
            """
            @purpose Returns the starting state
            """
            return self.starting

        def add_state(self, id, reference):
            """
            @purpose Prints the states image
            """
            try:
                print self.states[id]
                raise Exception("State already exists.")
            except KeyError:
                self.states[id] = reference
                print self.states

        def get_state(self, id):
            """
            @purpose Returns the state with the ID
            :param id: ID of the state
            """
            return self.states[id]

        def delete_state(self, id):
            """
            @purpose Deletes the state that was selected
            :param id: ID of the state that was clicked on
            :return:
            """
            del self.states[id]

        def get_num_states(self):
            """
            @purpose Returns the number of states
            """
            return len(self.states)

        def add_transition(self, origin, destination):
            #TODO: Transitions not needed for A3
            pass

        def delete_transition(self, origin, destination):
            #TODO: Transitions not needed for A3
            pass

        def modify_state(self,original_id,new_id):
            pass

        def reset_execution(self):
            # Resets the execution state of the turing machine
            self.current_step = 0
            self.current_read = None
            self.current_state = self.starting
            self.current_transition = None
            self.halted = False

        def execute(self):
            """
            @purpose When the "Execute" button is clicked, this will execute the Turing Machine by one step
            """
            if self.current_transition is not None:
                self.current_transition.execute_unhighlight()
            self.increment_step()
            self.current_read = self.tape.read()

            transitions = self.current_state.get_transition_seen(self.current_read)
            #print self.current_read

            print transitions
            if len(transitions) > 0:
                tran = random.choice(transitions)

                #for tran in transitions:
                self.current_transition = tran
                self.current_transition.execute_highlight()
                self.current_state = tran.get_end()
                self.write_current_pos(tran.get_write())
                move = tran.get_move()
                print tran.id, self.current_state.id
                if move == "L":
                    self.move_left()
                elif move == "R":
                    self.move_right()
                elif move == "N":
                    pass

                print(self.tape.head_pos, self.tape.tape)


            if len(transitions) == 0:
                # if no transition if defined for a particular symbol in a state, halts
                self.halt()

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



        def increment_step(self):
            """
            @purpose Maintains a counter of steps for a TM simulation
            """
            self.current_step += 1

        def write_current_pos(self, value):
            """
            @purpose Allows for writing data on the current position of the head
            :param value: The value to be written
            """
            return self.tape.write(value)

        def check_halt_answer(self):
            """
            @purpose Check whether the Turing Machine halts with a "Yes" or a "No".
            """
            print self.current_state.id
            if self.current_state.is_halt() is True:
                content= Label(text="Halted with answer YES")
                print "halted with answer yes"
            else:
                content= Label(text="Halted with answer NO")
                print "halted with answer no"

            self._popup = Popup(title="Execution Complete",
                            content=content,
                            size_hint=(0.3, 0.3))
            self._popup.open()


    """
    @purpose Main container class, containing various general UI handlers
    """
    def __init__(self, **kwargs):
        # Constructor
        super(Container, self).__init__(**kwargs)

        # Initialise Machine class used to keep track of states
        self.machine = self.Machine()
        self.xml_tree = None

        # Initialising edit mode flag
        self.edit_mode = False
        self.edit_mode_selected_state = None
        self._popup = None
        self.stepping = False

        # Initialise variables for use with Scatterlayout, setting maximum/min scaling,
        # Disabling single finger move canvas, disabling rotation
        Window.clearcolor = (0.7, 0.7, 0.7, 1)
        self.ids.layout_states.scale_max = 3.05175
        self.ids.layout_states.scale_min = 0.32768
        self.ids.layout_states.translation_touches = 2
        self.ids.layout_states.do_rotation = False
        self.zoom_counter = 0

        self.home_screen(self)

        self.state_size = (100,100)
        self.state_x_pos = 100
        self.state_y_pos = 100
        self.state_y_hint = 0.1

        self.xml_tree = None
        self._event = None


    def set_selected_halting_state(self):
        # Sets the selected state as Halting

        # First track all the incoming and outgoing transitions, as well as other state data
        selection = self.get_selection()
        transition = selection.get_transitions()
        incoming = selection.incoming_transitions
        arrow = selection.start_arrow
        arguments = selection.kw
        old_position = selection.pos
        start_flag = False
        if selection == self.machine.get_starting_state():
            start_flag = True

        # Then remove the currently selected state
        self.remove_selected_state(True)


        # Now recreate another state based on the saved data, but make it halting instead
        new = self.create_state(arguments.get('id',0),True)
        new.pos = old_position
        new.children[0].pos = old_position
        new.start_arrow = arrow
        new.transitions = transition
        new.incoming_transitions = incoming
        new.update_transitions_nodes()
        if start_flag is True:
            self.machine.set_starting(new.id)



    def select(self, new):
        # Method for handling selection of a state
        # Handles the updating of the Edit Mode menu as well

        edit_bar = self.children[0]
        if self.edit_mode is True:
            if new is None:
                self.edit_mode_selected_state = None
                edit_bar.ids.del_button.text = "Delete State"
                edit_bar.ids.make_initial_button.text = "Make Starting"
                edit_bar.ids.make_halting_button.text = "Make Halting"
                edit_bar.ids.add_tran_button.text = "Add Transition from.."
            else:
                if self.edit_mode_selected_state is not None:
                    self.edit_mode_selected_state.selection(False)
                self.edit_mode_selected_state = new
                edit_bar.ids.del_button.text = "Delete " + new.id
                edit_bar.ids.make_initial_button.text = "Make " + new.id + " Starting"
                edit_bar.ids.make_halting_button.text = "Make " + new.id + " Halting"
                edit_bar.ids.add_tran_button.text = "Transition " + new.id

    def set_tape(self, tape):
        # Method to set the initial contents of the tape

        if tape is not None:
            self.machine.set_tape(tape)
            self.redraw_tape()
        else:
            tape = ""
            for _ in range(15):
                tape += "b"
            tape = "  ".join(tape)
            self.ids.tape_layout.children[0].children[0].text = tape


    def redraw_tape(self):
        # Method to update the visual display of the tape

        tape = self.machine.get_tape()
        if len(tape) < 15:
            for _ in range(15-len(tape)):
                tape += "b"
        tape = "  ".join(tape)
        pos = self.machine.get_current_tape_head_pos()
        tape = tape[0:3*pos] + "[" + tape[3*pos] + "]" + tape[3*pos+1:]
        self.ids.tape_layout.children[0].children[0].text = tape

    def get_selection(self):
        # Returns the currently selected state reference
        if self.edit_mode:
            return self.edit_mode_selected_state
        else:
            return None

    def remove_selected_state(self, replace_flag=False):
        # Deletes the currently selected state
        # Replace_Flag is true, used for cases where the state is being replaced with a halting/starting version

        if self.edit_mode_selected_state is not None:
            if replace_flag is False:
                name = self.edit_mode_selected_state.id
                self.edit_mode_selected_state.remove_self()
                self.machine.delete_state(name)

                self.ids.layout_states.remove_widget(self.edit_mode_selected_state)
                self.select(None)
            else:
                name = self.edit_mode_selected_state.id
                self.machine.delete_state(name)
                self.ids.layout_states.remove_widget(self.edit_mode_selected_state)
                self.select(None)

    def add_transition(self, origin, end, seen, write, move):
        # Add a transition, from origin, to the end state, when seen SYMBOL, write SYMBOL, and move direction L/R/N

        if origin is None:
            origin = self.get_selection().id

        origin =self.machine.get_state(origin)
        end_node = self.machine.get_state(end)

        offset = 0
        for key,value in origin.get_transitions().iteritems():
            for t in value:
                if t.end_node == end_node:
                    offset += 1

        transition = UIObj_Transition(id=str(end+": "+seen+"/"+write+","+move),
                                        start=origin,
                                        end=end_node,
                                        seen=seen,
                                        write=write,
                                        move=move,
                                      offset=offset)
        self.ids.layout_states.add_widget(transition)
        origin.add_transition(transition)
        end_node.add_incoming_transition(transition)



    def home_screen(self, obj):
        # Method to handle displaying of the main home menu for loading or creating new files

        if self._popup is not None:
            self._popup.dismiss()

        self.home_popup = Popup(title="Turing Machine Simulator",
                            content=HomeScreenWindow(),
                            size_hint=(1, 1),
                            auto_dismiss=False)

        load_button = self.home_popup.content.ids.home_load
        new_dtm_button = self.home_popup.content.ids.home_new_dtm

        load_button.bind(on_release=self.load_handler)
        new_dtm_button.bind(on_release=self.create_new_handler)

        # Reveal dialog
        Clock.schedule_once(self.home_popup.open, 0.5)


    def create_new_handler(self, obj):
        self.reset_container()
        self.edit_mode_controller(True)
        self.home_popup.dismiss()


    def load_handler(self, obj):
        """
        @purpose Shows a file browser dialog for user to pick an XML file
        """
        self._popup = Popup(title="Load a Turing Machine XML File",
                            content=BrowseFileChooserWindow(),
                            size_hint=(0.85, 0.85))

        # Assign handler on dismiss
        self._popup.bind(on_dismiss=self.after_load_handler)
        self._popup.content.ids.cancel_button.bind(on_release=self._popup.dismiss)

        # Reveal dialog
        self._popup.open()

    def reset_container(self):
        # Method to reinitialise the display container
        self.xml_tree = None
        self.reset_state_pos()
        self.zoom_reset()
        self.ids.layout_states.pos = (0,0)
        self.ids.layout_states.clear_widgets()
        self.machine = self.Machine()
        self.set_tape(None)

    def after_load_handler(self, obj):
        """
        @purpose To handle loading file and data from XML file
        """

        # Check if the user has selected a file to load from
        if obj.content.path is not None:
            self.home_popup.dismiss()

            # Initialising UI variables, clearing canvas and setting the stage
            self.reset_container()
            board = self.ids.layout_states

            # reading from XML file
            xml_tree = ET.parse(obj.content.path)
            self.xml_tree = xml_tree
            try:
                self.machine = self.Machine(xml_tree.find("blank").attrib["char"])

                xml_states = xml_tree.find("states")

                end_states_names = []
                for s in xml_tree.find("finalstates"):
                    end_states_names.append(s.attrib["name"])

                # Start looping through the XML file
                for child in xml_states:
                    # If halt, create halt object, else create ordinary state object
                    if child.attrib["name"] in end_states_names:
                        new = self.create_state(child.attrib["name"], True)
                    else:
                        new = self.create_state(child.attrib["name"], False)


                initial_state_name = xml_tree.find("initialstate").attrib["name"]
                start_node = self.machine.get_state(initial_state_name)
                self.set_starting_state(start_node)

                for child in xml_states:
                    for tran in child:
                        origin = child.attrib["name"]
                        end = tran.attrib["newstate"]
                        seen = tran.attrib["seensym"]
                        write = tran.attrib["writesym"]
                        move = tran.attrib["move"]
                        self.add_transition(origin, end, seen, write, move)

                self.set_tape(xml_tree.find("initialtape").text)
            except AttributeError:
                self._popup = Popup(title="Error Loading File",
                                    content=Label(text="Please try again with a valid XML file."),
                                    size_hint=(0.8, 0.3))
                self._popup.open()


    def reset_state_pos(self):
        """
        @purpose To reset the state position to the initial position
        """
        self.state_y_pos = 100
        self.state_x_pos = 100
        self.state_y_hint = 0.1

    def update_state_pos(self):
        """
        @purpose To update the state position
        """
        win_x, win_y = Window.size
        padding = 70
        self.state_x_pos += (self.state_size[0]+padding)
        if self.state_x_pos > Window.size[0]:
            self.state_x_pos = 100  #+((self.state_size[0]+padding))
            self.state_y_hint += 0.1
            self.state_y_pos = win_y*self.state_y_hint

    def create_state(self, name, halting):
        """
        @purpose Creating states
        """
        # Initialising appearance variables for States
        if len(name) > 0:
            board = self.ids.layout_states
            if halting is True:
                state = UIObj_State_Halting(id=str(name),
                                                    x = self.state_x_pos,
                                                    y = self.state_y_pos,
                                                    size=self.state_size)
            else:
                state = UIObj_State(id=str(name),
                                                    x = self.state_x_pos,
                                                    y = self.state_y_pos,
                                                    size=self.state_size)

            self.machine.add_state(str(name),state)
            board.add_widget(state)
            self.update_state_pos()
            return state
        else:
            raise Exception


    def close_handler(self):
        self.execute_stop()
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

    def get_starting_state(self):
        """
        @purpose Returns the starting state
        """
        return self.machine.get_starting_state()

    def set_starting_state(self, state):
        """
        @purpose: Set the new starting state to the one that was clicked on
        :param state: Takes in the state that was clicked on
        """
        old = self.machine.get_starting_state()
        if old is not None:
            arrow = old.remove_start_arrow()
            self.ids.layout_states.remove_widget(arrow)


        self.machine.set_starting(state.id)
        initial_state = self.machine.get_starting_state()
        arrow = UIObj_StartArrow(node=initial_state)
        self.ids.layout_states.add_widget(arrow)
        state.add_start_arrow(arrow)
        self.select(initial_state)

    def dismiss_popup(self):
        self._popup.dismiss()

    def save_handler(self):
        """
        @purpose: Pops up the Save window
        """
        content = SaveFileChooserWindow(save=self.after_save_handler, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def after_save_handler(self, path, filename):
        """
        @purpose: Saves the Turing Machine to an XML file
        :param path: Takes in the path
        :param filename: Takes in the filename that was keyed in
        :return:
        """
        #Handler for  save button, saves the customised Turing machine to xml
        # Check if currently there is a xml file loaded
        # if there is currently a xml loaded, update the xml file in 1.xml
        # else, create a new turing machine xml file in 1.xml

        # TO-DO: User input the name of the file. For now it's all 1.xml
        # if self.xml_tree is not None:
        # If currently there is a xml loaded
        # get the current xml tree, and remove all the states

        if filename is not None and path is not None:
            new_tree = self.generate_memory_etree()

            xml = prettify(new_tree.getroot())
            print xml

            self._popup.dismiss()
            if filename[-4::] != ".xml":
                filename = filename + ".xml"
            fn = os.path.join(path, filename)
            print fn
            try:
                open(fn,'w').write(xml)
                message = "File saved in " + str(filename)
            except IOError:
                print("Error")
                message = "There was an error saving file. Please try again with a valid path or filename."

            self._popup = Popup(title="Save File",
                                content=Label(text=message),
                                size_hint=(0.9,0.3))
            self._popup.open()




    def generate_memory_etree(self):
        """
        @purpose: Convert XML file to the Element Tree
        """
        if self.xml_tree is not None:
            xml_tree = self.xml_tree
        else:
            xml_tree = Element("turingmachine")
            SubElement(xml_tree,"alphabet")
            SubElement(xml_tree,"initialtape")
            SubElement(xml_tree,"blank", {'char':'b'})
            SubElement(xml_tree,"initialstate")
            SubElement(xml_tree,"finalstates")
            SubElement(xml_tree,"states")
            xml_tree = ElementTree(xml_tree)

        xml_tree.find("initialtape").text = self.machine.get_tape()
        if self.machine.get_starting_state() is not None:
            xml_tree.find("initialstate").attrib["name"] = self.machine.get_starting_state().id
        final = xml_tree.find("finalstates")
        for state in final.findall("finalstate"):
            final.remove(state)
        for key,value in self.machine.states.iteritems():
            if value.is_halt():
                final.append(Element("finalstate",
                                     {"name":value.id}))

        xml_states = xml_tree.find("states")
        for state in xml_states.findall("state"):
                xml_states.remove(state)
        for key,value in self.machine.states.iteritems():
                state = Element("state", {"name":value.id})

                for key,transitions in value.get_transitions().iteritems():
                    for transition in transitions:
                        state.append(Element("transition",
                                             {"seensym":transition.get_seen(),
                                              "writesym": transition.get_write(),
                                              "newstate": transition.get_end().id,
                                              "move": transition.get_move()}))

                xml_states.append(state)

        return xml_tree

    def edit_handler(self, button):
        """
        @purpose: Handles the edit button click
        """

        # Condition checks if we are currently in edit mode
        if self.edit_mode is True:
            self.edit_mode_controller(False)
        else:
            self.edit_mode_controller(True)


    def edit_mode_controller(self, flag):
        """
        @purpose: Shows or hides the edit mode toolbar.
        """
        button = self.ids.edit_button

        if flag is False:

            if button is not None:
                button.text = "Edit"

            self.children[0].canvas.clear()

            self.remove_widget(self.children[0])
            self.edit_mode = False
            if self.edit_mode_selected_state is not None:
                self.edit_mode_selected_state.selection(False)


            self.edit_mode_selected_state = None
        else:
            if button is not None:
                button.text = "Done"

            self.edit_mode = True

            # Shows the customisation toolbar
            bl = UIObj_Edit()
            self.add_widget(bl)
            bl.children[0].pos = 0,-100
            anim = Animation(x=0, y=0, duration=0.2)
            anim.start(bl.children[0])


    def zoom_handler(self, text):
        """
        @purpose: Handles the zoom buttons
        :param text: Takes in the zoom text
        :return:
        """
        if text == "Zoom In":
            if self.ids.layout_states.scale < 3.05175:
                mat = Matrix().scale(1.25,1.25,1.25)
                self.ids.layout_states.apply_transform(mat)
        elif text == "Zoom Out":
            if self.ids.layout_states.scale > 0.32768:
                mat = Matrix().scale(0.8,0.8,0.8)
                self.ids.layout_states.apply_transform(mat)


    def zoom_reset(self):
        """
        @purpose: Reset the states to the original position
        """
        self.ids.layout_states.pos = [0,0]
        self.zoom_counter = 0
        factor = 1/self.ids.layout_states.scale
        mat = Matrix().scale(factor, factor, factor)
        self.ids.layout_states.apply_transform(mat)


    def about_handler(self):
        """
        @purpose: Handles the 'About' button
        """
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="TuringSim v0.3, \nby Loh Hao Bin, Ashley Ong Yik Mun & Varshinee Servansingh\nFIT3140 Advanced Programming, Semester 2, 2015"))

        self._popup = Popup(title="About TuringSim",
                            content=content,
                            size_hint=(0.6, 0.3))

        self._popup.open()

    def execute_handler(self,text):
        """
        @purpose: Handles the 'Execute' button
        :param text: Takes in the text button
        :return:
        """
        if text == "Execute":
            if self.edit_mode is True:
                self.edit_mode_controller(False)
            if self.stepping is False:
                self.machine.reset_execution()
            self.execute()

        elif text == "Stop":
            self.execute_stop()

    def execute(self, value=None):
        """
        @purpose: Executes the Turing Machine.
        """
        if self.machine.get_num_states() > 0:
            if self.machine.current_state is not None:
                self.ids.edit_button.disabled = True
                self.ids.save_button.disabled = True

                self.machine.current_state.execute_current_state_restore()
                if self.machine.is_halted() is False:
                    self.machine.execute()
                    self.redraw_tape()
                    self.machine.current_state.execute_current_state()
                    if value != "step_mode":
                        self.ids.execute_button.text = "Stop"
                        self.ids.step_button.disabled = True
                        self._event = Clock.schedule_once(self.execute, 0.5)
                else:
                    self.execute_stop()
                    self.machine.check_halt_answer()
        else:
            self._popup = Popup(title="No State Added",
                                content=Label(text="Please add at least one state to proceed"),
                                size_hint=(0.8, 0.3))
            self._popup.open()

    def execute_stop(self):
        # self._event is not None and
        if self.machine.current_state is not None:
            self.ids.execute_button.text = "Execute"
            if self._event is not None:
                Clock.unschedule(self._event)
            self.ids.edit_button.disabled = False
            self.ids.step_button.disabled = False
            self.ids.save_button.disabled = False

    def step_through_handler(self):
        self.stepping = True
        self.execute("step_mode")
