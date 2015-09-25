__author__ = 'HaoBin'

from kivy.uix.widget import Widget
from kivy.uix.label import Label

from kivy.properties import ObjectProperty

from ui_lib import *

class UIObj_Edit(Widget):
    # This object is for edit mode toolbar usage
    edit = ObjectProperty(None)
    size = Window.size[0], 100

    def __init__(self, **kwargs):
        self.selected = None
        super(UIObj_Edit,self).__init__(**kwargs)

    def select(self):
        pass

    def add_state(self):
        content = BoxLayout(orientation="vertical")
        textinput = TextInput(hint_text='State Name', multiline=False, id='textinput')
        button = Button(text="Add State")
        content.add_widget(textinput)
        content.add_widget(button)

        self._popup = Popup(title="Enter New Transition Name",
                            content=content,
                            size_hint=(0.3, 0.3))
        textinput.bind(on_text_validate=self.on_enter_add)
        button.bind(on_release=self.on_ok_button_add)
        self._popup.open()

    def on_enter_add(self, value):
        halting = False
        self.add_state_handler(self._popup.content.children[1].text, halting)

    def on_ok_button_add(self, value):
        halting = False
        self.add_state_handler(self._popup.content.children[1].text, halting)

    def add_state_handler(self, name, halting):
        try:
            self.parent.create_state(name, halting)
            self._popup.dismiss()
        except Exception:
            self._popup.title = "Name Error"
            self._popup.content.children[1].text = ""

    def delete_state(self):
        selection = self.get_parent_window().children[0].get_selection()
        if selection is not None:
            content = BoxLayout(orientation="horizontal")
            button_ok = Button(text="Delete")
            button_cancel = Button(text="Cancel")
            content.add_widget(button_ok)
            content.add_widget(button_cancel)

            message = "Delete " + selection.id + "?"
            self._popup = Popup(title=message,
                                content=content,
                                size_hint=(0.3, 0.3))
            button_ok.bind(on_release=self.delete_state_proceed)
            button_cancel.bind(on_release=self._popup.dismiss)
            self._popup.open()



        else:
            self._popup = Popup(title="Warning",
                                content=Label(text="Please select a state"),
                                size_hint=(0.3, 0.3))
            self._popup.open()

    def delete_state_proceed(self, value):
        self.parent.remove_selected_state()
        self._popup.dismiss()

    def add_tran_button(self):
        selection = self.get_parent_window().children[0].get_selection()
        if selection is not None:
            content = BoxLayout(orientation="vertical")


            dest_input = TextInput(hint_text='Destination State', multiline=False)
            read_input = TextInput(hint_text='Read', multiline=False)
            write_input = TextInput(hint_text='Write', multiline=False)
            move_input = TextInput(hint_text='Move (L/R/N)', multiline=False)
            button = Button(text="Add Transition")
            content.add_widget(dest_input)
            content.add_widget(read_input)
            content.add_widget(write_input)
            content.add_widget(move_input)
            content.add_widget(button)

            origin = selection.id
            string = "Enter New Transition from " + origin
            self._popup = Popup(title=string,
                                content=content,
                                size_hint=(0.3, 0.4))
            button.bind(on_release=self.on_ok_button_add_tran)
            self._popup.open()
        else:
            self._popup = Popup(title="Warning",
                                content=Label(text="Please select a state"),
                                size_hint=(0.3, 0.3))
            self._popup.open()

    def on_ok_button_add_tran(self, value):
        self._popup.dismiss()
        print("x")

        print self._popup.content.children
        end = self._popup.content.children[4].text
        seen = self._popup.content.children[3].text
        write =self._popup.content.children[2].text
        move = self._popup.content.children[1].text
        self.parent.add_transition(None, end, seen, write, move)

    def make_initial_state(self):
        selection = self.get_parent_window().children[0].get_selection()
        if selection is not None:
            self.parent.set_starting_state(self.parent.get_selection())
        else:
            self._popup = Popup(title="Warning",
                                content=Label(text="Please select a state"),
                                size_hint=(0.3, 0.3))
            self._popup.open()

    def make_halting_state(self):
        selection = self.get_parent_window().children[0].get_selection()
        if selection is not None:
            self.parent.set_selected_halting_state()
        else:
            self._popup = Popup(title="Warning",
                                content=Label(text="Please select a state"),
                                size_hint=(0.3, 0.3))
            self._popup.open()

    def set_tape(self):
        content = BoxLayout(orientation="vertical")
        textinput = TextInput(hint_text='Use b for blank, e.g bb010101bbb', multiline=False, id='textinput')
        button = Button(text="Set Tape")
        content.add_widget(textinput)
        content.add_widget(button)

        self._popup = Popup(title="Set custom tape",
                            content=content,
                            size_hint=(0.4, 0.3))
        button.bind(on_release=self.on_ok_button_set_tape)
        self._popup.open()

    def on_ok_button_set_tape(self, value):
        tape = self._popup.content.children[1].text

        self._popup.dismiss()
        self.parent.set_tape(tape)



