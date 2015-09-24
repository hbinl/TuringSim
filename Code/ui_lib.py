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
#from kivy.graphics import Color, Ellipse, Rectangle, Line
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
        self.kw = kwargs

        self.transitions = {}
        self.incoming_transitions = []
        self.selected = False

        self.ishalt = False
        self.menu_visible = False
        self.start_arrow = None

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
                              font_size=20,
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
            print(self.incoming_transitions)
            self.pos = touch.x-25, touch.y-25
            self.children[0].pos = touch.x-25, touch.y-25
            if self.start_arrow is not None:
                self.update_start_arrow(self.pos)
            for key,value in self.transitions.iteritems():
                for t in value:
                    t.redraw()
            for incoming in self.incoming_transitions:
                incoming.redraw()




    def on_touch_up(self, touch):
        # upon user's release of the item
        if touch.grab_current is self:
            touch.ungrab(self)


    def is_halt(self):
        return self.halting

    def add_transition(self, transition):
        seen = transition.get_seen()
        print self.transitions
        try:
            self.transitions[seen] += [transition]
        except KeyError:
            self.transitions[seen] = []
            self.transitions[seen].append(transition)


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

    def add_start_arrow(self, arrow_reference):
        self.start_arrow = arrow_reference

    def update_start_arrow(self, touch):
        self.start_arrow.redraw(touch)

    def get_transitions(self):
        return self.transitions

    def quick_set_transitions(self, tran):
        self.transitions = tran

    def get_center(self):
        return self.center

    def add_incoming_transition(self, tran):
        self.incoming_transitions.append(tran)


    def update_transitions_nodes(self):
        for key,value in self.transitions.iteritems():
                for t in value:
                    t.update_origin(self)
        for incoming in self.incoming_transitions:
            incoming.update_end(self)

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

        self.id=kwargs.get('id',0)
        self.seen=kwargs.get('seen',0)
        self.write=kwargs.get('write',0)
        self.move=kwargs.get('move','N')

        self.start_node = kwargs.get('start',0)
        self.end_node = kwargs.get('end',0)

        super(UIObj_Transition,self).__init__(**kwargs)

        self.redraw()

    def get_seen(self):
        return self.seen

    def redraw(self):
        print self.start_node, self.end_node
        self.canvas.before.clear()
        self.canvas.before.add(Color(0,0,0))
        self.canvas.before.add(Line(bezier=(self.start_node.get_center()[0],
                                            self.start_node.get_center()[1],
                                            (self.start_node.get_center()[0]+self.end_node.get_center()[0])/2+50,
                                            (self.start_node.get_center()[1]+self.end_node.get_center()[1])/2+77,
                                            self.end_node.get_center()[0],
                                            self.end_node.get_center()[1]),
                             width=1))

    def update_origin(self, node):
        self.start_node = node

    def update_end(self, node):
        self.end_node = node


class UIObj_StartArrow(Widget):
    start = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.node = kwargs.get('node',0)
        self.origin_x = self.node.x+15
        self.origin_y = self.node.y+80
        super(UIObj_StartArrow,self).__init__(**kwargs)

        self.redraw(None)

    def redraw(self, node):
        if node is not None:
            self.origin_x = node[0]+15
            self.origin_y = node[1]+80

        self.canvas.clear()
        self.canvas.add(Color(0,0,0))
        self.canvas.add(Line(bezier=(self.origin_x, self.origin_y, self.origin_x-50, self.origin_y+50), width=3))
        self.canvas.add(Triangle(points=(self.origin_x, self.origin_y, self.origin_x-20, self.origin_y,self.origin_x, self.origin_y+20)))



