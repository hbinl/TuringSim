"""
@title FIT3140 Assignment 3 Spikes - UI classes
@description Spike test, contains Spike 2, 3 and 4

            #######################################################
            To look for codes related to a particular spike,
            just find "Spike1", "#Spike2", "#Spike3" or "#Spike4"
            #######################################################

@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 1/9/2015
"""
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

import os
import xml.etree.ElementTree as ET


################## SPIKE 2 ###################

#Spike2
class UIObj_State(Widget):
    """
    @purpose UI Object class for States' visual representation
    @kivyparams
        - size: diameter of the state, handled by the caller
        - x & y: calculated position of the state (handled by the caller)
        - id: Name of the state, will be used for label
    """
    state = ObjectProperty(None)

    def __init__(self, **kwargs):
        # initialising some basic information about the states
        self.ishalt = False
        self.menu_visible = False
        self.size_hint_y = 0
        self.size_hint_x = 0
        self.selected = False
        self.size= kwargs.get('size',0)
        self.x = kwargs.get('x',0)
        self.y = kwargs.get('y',0)
        self.id = kwargs.get('id',0)
        super(UIObj_State,self).__init__(**kwargs)

        # Adding name label to the state
        self.add_widget(Label(text=str(self.id),
                              pos=(self.center_x-(self.size[0]/2), self.center_y-(self.size[1]/2)),
                              size=(100,100),
                              size_hint=(None, None)))

    def on_touch_down(self, touch):
        # handler for touch events, using collide point to check if inside State boundary
        if self.menu_visible:
            self.menu_visible = False
            self.get_parent_window().children[0].ids.container_rl.remove_widget(self.menu)
        if self.collide_point(touch.x,touch.y):

            if self.get_parent_window().children[0].edit_mode:
                touch.grab(self)
                print("Creating Transitions")
                self.children[0].text = str(self.id + "*")
                self.selected = True
                if self.menu_visible is False:
                    self.menu_visible = True
                    self.menu = UI_LongTouch_Menu(pos=touch.pos, state_ref=self)

                    self.get_parent_window().children[0].ids.container_rl.add_widget(self.menu)
            return True


    def on_touch_move(self, touch):
        # when it moves...
        if touch.grab_current is self:
            self.pos = touch.x-25, touch.y-25
            self.children[0].pos = touch.x-25, touch.y-25


    def on_touch_up(self, touch):
        # upon user's release of the item
        if touch.grab_current is self:
            touch.ungrab(self)
            self.children[0].text = str(self.id)

#Spike2
class UIObj_State_Halting(UIObj_State):
    """
    @purpose UI Object class for Halting States' visual representation, based
            on inherited implementation of UIObj_State
    @kivyparams
        - size: diameter of the state, handled by the caller
        - x & y: calculated position of the state (handled by the caller)
        - id: Name of the state, will be used for label
    """
    state = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(UIObj_State_Halting,self).__init__(**kwargs)
        self.ishalt = True



#Spike3
class UIObj_Edit(Widget):
    # This object is for edit mode toolbar usage
    edit = ObjectProperty(None)


#Spike3 MENU
class UI_LongTouch_Menu(Widget):
    # Object for the State Menu items in Edit Mode
    # Allowing the user to delete and customise states
    menu = ObjectProperty(None)
    def __init__(self, **kwargs):
        self.pos = kwargs.get('pos',(100,0))
        self.state_ref = kwargs.get('state_ref',None)

        super(UI_LongTouch_Menu,self).__init__(**kwargs)

    def delete_state(self):
        # Handler for delete state button
        if self.state_ref is not None:
            self.get_parent_window().children[0].machine.delete_state(self.state_ref.id)
            self.get_parent_window().children[0].ids.layout_states.remove_widget(self.state_ref)
            #print self.get_parent_window().children[0].machine.states



# UNUSED
# class UIObj_Transition(Widget):
#     transition = ObjectProperty(None)
#
#     def __init__(self, **kwargs):
#         self.origin_x = kwargs.get('origin_x',0)
#         self.origin_y = kwargs.get('origin_y',0)
#         self.end_x = kwargs.get('end_x',0)
#         self.end_y = kwargs.get('end_y',0)
#         self.width = kwargs.get('width',3)
#         self.tid = kwargs.get('tid',"nil")
#         self.is_self_state = kwargs.get('is_self_state', False)
#         self.mid_x = (self.origin_x+self.end_x)/2
#         self.mid_y = (self.origin_y+self.end_y)/2
#         super(UIObj_Transition,self).__init__(**kwargs)




#Spike3
class UIObj_State_Template(UIObj_State):
    """
    @purpose UI Object class for Halting States' visual representation, based
            on inherited implementation of UIObj_State
    @kivyparams
        - size: diameter of the state, handled by the caller
        - x & y: calculated position of the state (handled by the caller)
        - id: Name of the state, will be used for label
    """
    state = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(UIObj_State_Template,self).__init__(**kwargs)
        self.ishalt = False


    def on_touch_down(self, touch):
        # For Edit Mode template objects, this function upon activation,
        # creates a new copy of State object, and passes control over to the new object
        # Then the user can drag the object and add it to the canvas

        # handler for touch events, using collide point to check if inside State boundary
        if self.collide_point(touch.x,touch.y):
            touch.grab(self)

            # Create new object...
            copy_name = str("new"+str(touch.x+touch.y))
            copy = UIObj_State(id=copy_name, x = touch.x, y = touch.y, size=(100,100))

            # Adding it to UI and keeping track in memory
            self.parent.parent.ids.layout_states.add_widget(copy)
            self.get_parent_window().children[0].machine.add_state(copy_name, copy)

            # Passing control over...
            touch.ungrab(self)
            touch.grab(copy)

    def on_touch_move(self, touch):
        # when it moves...
        if touch.grab_current is self:
            self.pos = touch.x-25, touch.y-25
            self.children[0].pos = touch.x-25, touch.y-25


    def on_touch_up(self, touch):
        # upon user's release of the item
        if touch.grab_current is self:
            touch.ungrab(self)


#Spike3
class UIObj_State_Halting_Template(UIObj_State_Template):
    """
    @purpose UI Object class for Halting States' visual representation, based
            on inherited implementation of UIObj_State
    @kivyparams
        - size: diameter of the state, handled by the caller
        - x & y: calculated position of the state (handled by the caller)
        - id: Name of the state, will be used for label
    """
    state = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(UIObj_State_Halting_Template,self).__init__(**kwargs)
        self.ishalt = True

    def on_touch_down(self, touch):
        # For Edit Mode template objects, this function upon activation,
        # creates a new copy of State object, and passes control over to the new object
        # Then the user can drag the object and add it to the canvas


        # handler for touch events, using collide point to check if inside State boundary
        if self.collide_point(touch.x,touch.y):
            touch.grab(self)

            # Create new object...
            copy_name = str("halt"+str(touch.x+touch.y))
            copy = UIObj_State_Halting(id=copy_name, x = touch.x, y = touch.y, size=(100,100))

            # Adding it to UI and keeping track in memory
            self.parent.parent.ids.layout_states.add_widget(copy)
            self.get_parent_window().children[0].machine.add_state(copy_name, copy)

            # Passing control over...
            touch.ungrab(self)
            touch.grab(copy)
