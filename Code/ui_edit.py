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
        textinput = TextInput(text='State1', multiline=False, id='textinput')
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

    def add_tran_button(self):
        pass

    def delete_state(self):
        self.get_parent_window().children[0].remove_selected_state()


    def make_initial_state(self):
        pass

    def make_halting_state(self):
        pass

    def set_tape(self):
        pass

#
# class UI_LongTouch_Menu(Widget):
#     # Object for the State Menu items in Edit Mode
#     # Allowing the user to delete and customise states
#     menu = ObjectProperty(None)
#
#     def __init__(self, **kwargs):
#         self.pos = kwargs.get('pos',(100,0))
#         self.state_ref = kwargs.get('state_ref',None)
#
#         super(UI_LongTouch_Menu,self).__init__(**kwargs)
#         #self.ids.del_button.text = "Delete" + self.state_ref.id
#
#     def delete_state(self):
#         # Handler for delete state button
#         if self.state_ref is not None:
#             self.get_parent_window().children[0].edit_mode_selected_state = None
#             self.get_parent_window().children[0].machine.delete_state(self.state_ref.id)
#             self.get_parent_window().children[0].ids.layout_states.remove_widget(self.state_ref)
#             self.get_parent_window().children[0].ids.container_rl.remove_widget(self)
#
#             #print self.get_parent_window().children[0].machine.states


# class UIObj_State_Template(UIObj_State):
#     """
#     @purpose UI Object class for Halting States' visual representation, based
#             on inherited implementation of UIObj_State
#     @kivyparams
#         - size: diameter of the state, handled by the caller
#         - x & y: calculated position of the state (handled by the caller)
#         - id: Name of the state, will be used for label
#     """
#     state = ObjectProperty(None)
#
#     def __init__(self, **kwargs):
#         super(UIObj_State_Template,self).__init__(**kwargs)
#         self.ishalt = False
#
#
#     def on_touch_down(self, touch):
#         # For Edit Mode template objects, this function upon activation,
#         # creates a new copy of State object, and passes control over to the new object
#         # Then the user can drag the object and add it to the canvas
#
#         # handler for touch events, using collide point to check if inside State boundary
#         if self.collide_point(touch.x,touch.y):
#             touch.grab(self)
#
#             # Create new object...
#             copy_name = str("new"+str(touch.x+touch.y))
#             copy = UIObj_State(id=copy_name, x = touch.x, y = touch.y, size=(100,100))
#
#             # Adding it to UI and keeping track in memory
#             self.parent.parent.ids.layout_states.add_widget(copy)
#             self.get_parent_window().children[0].machine.add_state(copy_name, copy)
#
#             # Passing control over...
#             touch.ungrab(self)
#             touch.grab(copy)
#             #copy.initialise()
#
#     def on_touch_move(self, touch):
#         # when it moves...
#         if touch.grab_current is self:
#             self.pos = touch.x-25, touch.y-25
#             self.children[0].pos = touch.x-25, touch.y-25
#
#
#     def on_touch_up(self, touch):
#         # upon user's release of the item
#         if touch.grab_current is self:
#             touch.ungrab(self)
#
#
# class UIObj_State_Halting_Template(UIObj_State_Template):
#     """
#     @purpose UI Object class for Halting States' visual representation, based
#             on inherited implementation of UIObj_State
#     @kivyparams
#         - size: diameter of the state, handled by the caller
#         - x & y: calculated position of the state (handled by the caller)
#         - id: Name of the state, will be used for label
#     """
#     state = ObjectProperty(None)
#     def __init__(self, **kwargs):
#         super(UIObj_State_Halting_Template,self).__init__(**kwargs)
#         self.ishalt = True
#
#     def on_touch_down(self, touch):
#         # For Edit Mode template objects, this function upon activation,
#         # creates a new copy of State object, and passes control over to the new object
#         # Then the user can drag the object and add it to the canvas
#
#
#         # handler for touch events, using collide point to check if inside State boundary
#         if self.collide_point(touch.x,touch.y):
#             touch.grab(self)
#
#             # Create new object...
#             copy_name = str("halt"+str(touch.x+touch.y))
#             copy = UIObj_State_Halting(id=copy_name, x = touch.x, y = touch.y, size=(100,100))
#
#             # Adding it to UI and keeping track in memory
#             self.parent.parent.ids.layout_states.add_widget(copy)
#             self.get_parent_window().children[0].machine.add_state(copy_name, copy)
#
#             # Passing control over...
#             touch.ungrab(self)
#             touch.grab(copy)