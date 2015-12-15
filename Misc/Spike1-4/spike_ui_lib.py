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
            touch.grab(self)
            if self.get_parent_window().children[0].edit_mode:
                print("Creating Transitions")
                self.children[0].text = str(self.id + "*")
                self.selected = True
                if self.menu_visible is False:
                    self.menu_visible = True
                    self.menu = UI_LongTouch_Menu(pos=touch.pos)

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

################## SPIKE 3 ###################


#Spike3
class UIObj_Edit(Widget):
    edit = ObjectProperty(None)

#Spike3
class UI_LongTouch_Menu(Widget):
    menu = ObjectProperty(None)
    def __init__(self, **kwargs):
        self.pos = kwargs.get('pos',(100,0))

        super(UI_LongTouch_Menu,self).__init__(**kwargs)
        print self.parent


class UIObj_Transition(Widget):
    transition = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.origin_x = kwargs.get('origin_x',0)
        self.origin_y = kwargs.get('origin_y',0)
        self.end_x = kwargs.get('end_x',0)
        self.end_y = kwargs.get('end_y',0)
        self.width = kwargs.get('width',3)
        self.tid = kwargs.get('tid',"nil")
        self.is_self_state = kwargs.get('is_self_state', False)
        self.mid_x = (self.origin_x+self.end_x)/2
        self.mid_y = (self.origin_y+self.end_y)/2
        super(UIObj_Transition,self).__init__(**kwargs)



#Spike3
class UIObj_State_Halting_Template(UIObj_State_Halting):
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
        self.ishalt = False


    def on_touch_down(self, touch):
        # handler for touch events, using collide point to check if inside State boundary
        if self.collide_point(touch.x,touch.y):
            touch.grab(self)
            self.copy = UIObj_State_Halting(id=str("Halt"), x = touch.x, y = touch.y, size=(100,100))
            self.parent.parent.ids.layout_states.add_widget(self.copy)
            touch.ungrab(self)
            touch.grab(self.copy)
            print touch.grab_current

    def on_touch_up(self,touch):
        if touch.grab_current is self:
            touch.ungrab(self)

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
        # handler for touch events, using collide point to check if inside State boundary
        if self.collide_point(touch.x,touch.y):
            touch.grab(self)
            copy = UIObj_State(id=str("New"), x = touch.x, y = touch.y, size=(100,100))
            self.parent.parent.ids.layout_states.add_widget(copy)
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