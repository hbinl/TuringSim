"""
@title FIT3140 Assignment 5
@description Sprint 1
@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 1/9/2015
"""
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.button import Button
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
from kivy.uix.textinput import TextInput

from kivy.properties import ObjectProperty
import ui_edit


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


        self.transitions = {}
        self.selected = False

        self.ishalt = False
        self.menu_visible = False

        self.size_hint_y = 0
        self.size_hint_x = 0
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

        if self.collide_point(touch.x,touch.y):
            if self.get_parent_window().children[0].edit_mode:
                touch.grab(self)
                print("Grabbed", self.id)
                if self.selected is False:
                    self.selection(True)
                else:
                    self.selection(False)

            return True
        else:
            self.selection(False)


    def on_touch_move(self, touch):
        # when it moves...
        if touch.grab_current is self:
            self.pos = touch.x-25, touch.y-25
            self.children[0].pos = touch.x-25, touch.y-25


    def on_touch_up(self, touch):
        # upon user's release of the item
        if touch.grab_current is self:
            touch.ungrab(self)


    def is_halt(self):
        return self.halting

    def add_transition(self, end, seen, write, move):
        try:
            self.transitions[seen] += Transition(self.id, end, seen, write, move)

        except KeyError:
            self.transitions[seen] = [Transition(self.id, end, seen, write, move)]

    def get_transition_seen(self, seen):
        try:
            return self.transitions[seen]
        except KeyError:
            return []

    def selection(self, bool):
        if bool is True:
            self.selected = True
            self.children[0].text = str(self.id + "*")
            self.get_parent_window().children[0].select(self)
        else:
            self.selected = False
            self.children[0].text = str(self.id)
            self.get_parent_window().children[0].select(None)


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



class UIObj_Tape_Head(Widget):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            if (touch.x > Window.size[0] * 0.3) and (touch.x < Window.size[0]*0.71):
                self.center_x = touch.x

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)



class UIObj_Transition(Widget):
    transition = ObjectProperty(None)

    def __init__(self, **kwargs):

        super(UIObj_Transition,self).__init__(**kwargs)

