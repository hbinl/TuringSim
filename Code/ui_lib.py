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
from kivy.clock import Clock




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
        """
        @purpose: Initialising some basic information about the states
        """
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
        """
        @purpose: Handler for touch events, using collide point to check if inside State boundary
        """
        if self.collide_point(touch.x,touch.y):
            if self.get_parent_window().children[0].edit_mode:
                touch.grab(self)

                if self.selected is False:
                    self.selection(True)
                else:
                    self.selection(False)

            return True
        else:
            self.selection(False)


    def on_touch_move(self, touch):
        """
        @purpose: when the State moves
        """
        if touch.grab_current is self:

            self.pos = touch.x-25, touch.y-25
            self.children[0].pos = touch.x-25, touch.y-25
            if self.start_arrow is not None:
                self.update_start_arrow(self.pos)
            for key,value in self.transitions.iteritems():
                for t in value:
                    if t is not None:
                        t.redraw()
            for incoming in self.incoming_transitions:
                if incoming is not None:
                    incoming.redraw()

    def execute_current_state(self):
        """
        @purpose: To highlight the State in green, when the Turing Machine simulator is runnning.
        """
        self.canvas.before.clear()
        self.canvas.before.add(Color(0,1,0))
        self.canvas.before.add(Ellipse(pos=(self.pos[0]-10,self.pos[1]-10), size=(self.size[0]+20,self.size[1]+20)))

    def execute_current_state_restore(self):
        self.canvas.before.clear()



    def on_touch_up(self, touch):
        """
        @purpose: When the user release the State object
        """
        # upon user's release of the item
        if touch.grab_current is self:
            touch.ungrab(self)


    def is_halt(self):
        return self.ishalt

    def add_transition(self, transition):
        seen = transition.get_seen()
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
        """
        @purpose: Add the starting arrow for the starting State
        """
        self.start_arrow = arrow_reference

    def update_start_arrow(self, touch):
        """
        @purpose: Updates the starting arrow
        """
        self.start_arrow.redraw(touch)

    def remove_start_arrow(self):
        """
        @purpose: Remove the old starting arrow
        """
        old = self.start_arrow
        self.start_arrow = None
        return old

    def get_transitions(self):
        """
        @purpose: Returns Transition
        """
        return self.transitions

    def quick_set_transitions(self, tran):
        """
        @purpose: Set transitions to tran
        """
        self.transitions = tran

    def get_center(self):
        """
        @purpose: Returns center
        """
        return self.center

    def add_incoming_transition(self, tran):
        """
        @purpose: Add transition
        """
        self.incoming_transitions.append(tran)


    def update_transitions_nodes(self):
        """
        @purpose: Updates the transition
        """
        for key,value in self.transitions.iteritems():
            for t in value:
                t.update_origin(self)
        for incoming in self.incoming_transitions:
            incoming.update_end(self)


    def remove_self(self):
        """
        @purpose: Delete transition
        """
        print("X")
        for key,value in self.transitions.iteritems():
            for t in value:
                t.parent.remove_widget(t)
                del t
        for incoming in self.incoming_transitions:
            print incoming.parent
            origin = incoming.get_origin().get_transitions()
            if incoming.get_loop() is False and incoming.parent is not None:
                incoming.parent.remove_widget(incoming)



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




class UIObj_Transition(Widget):
    """
    @purpose UI Object class for Transition visual representation
    """
    transition = ObjectProperty(None)

    def __init__(self, **kwargs):

        self.id=kwargs.get('id',0)
        self.seen=kwargs.get('seen',0)
        self.write=kwargs.get('write',0)
        self.move=kwargs.get('move','N')

        self.start_node = kwargs.get('start',0)
        self.end_node = kwargs.get('end',0)
        self.offset = kwargs.get('offset',0)*(-20)

        super(UIObj_Transition,self).__init__(**kwargs)

        self.loop = False
        if self.start_node == self.end_node:
            self.loop = True

        #Adding name label to the state
        self.add_widget(Label(text=str(self.id),
                              pos=(self.center_x-(self.size[0]/2)+self.offset, self.center_y-(self.size[1]/2)+self.offset),
                              size=(100,100),
                              font_size=20,
                              size_hint=(None, None)))
        self.redraw()

    def get_loop(self):
        """
        @purpose: Returns loop
        """
        return self.loop

    def get_seen(self):
        """
        @purpose: Returns seen
        """
        return self.seen

    def get_origin(self):
        """
        @purpose: Returns the start node
        """
        return self.start_node

    def get_end(self):
        """
        @purpose: Returns the end node
        """
        return self.end_node

    def get_write(self):
        """
        @purpose: Returns write
        """
        return self.write

    def get_move(self):
        """
        @purpose: Returns move
        """
        return self.move

    def redraw(self):
        """
        @purpose: Redraw a transition
        """
        if self.loop:
            self.canvas.before.clear()
            self.canvas.before.add(Color(0,0,0))
            self.canvas.before.add(Line(bezier=(self.start_node.get_center()[0],
                                                self.start_node.get_center()[1],
                                                (self.start_node.get_center()[0]+self.end_node.get_center()[0])/2+150,
                                                (self.start_node.get_center()[1]+self.end_node.get_center()[1])/2+207,
                                                (self.start_node.get_center()[0]+self.end_node.get_center()[0])/2+280,
                                                (self.start_node.get_center()[1]+self.end_node.get_center()[1])/2+17,
                                                self.end_node.get_center()[0],
                                                self.end_node.get_center()[1]),
                                 width=1))
            self.children[0].pos =  (self.start_node.get_center()[0]+self.end_node.get_center()[0])/2+120+self.offset,  (self.start_node.get_center()[1]+self.end_node.get_center()[1])/2+57+self.offset

        else:
            self.canvas.before.clear()
            self.canvas.before.add(Color(0,0,0))
            self.canvas.before.add(Line(bezier=(self.start_node.get_center()[0],
                                                self.start_node.get_center()[1],
                                                (self.start_node.get_center()[0]+self.end_node.get_center()[0])/2+50,
                                                (self.start_node.get_center()[1]+self.end_node.get_center()[1])/2+77,
                                                self.end_node.get_center()[0],
                                                self.end_node.get_center()[1]),
                                 width=1))
            self.children[0].pos =  (self.start_node.get_center()[0]+self.end_node.get_center()[0])/2+self.offset,  (self.start_node.get_center()[1]+self.end_node.get_center()[1])/2+self.offset

    def update_origin(self, node):
        """
        @purpose: Updates the start node
        """
        self.start_node = node

    def update_end(self, node):
        """
        @purpose: Updates the end node
        """
        self.end_node = node

    def execute_highlight(self):
        self.children[0].color = (0,1,0.5,1)
        Clock.schedule_once(self.execute_unhighlight,1)

    def execute_unhighlight(self, value=None):
        self.children[0].color = (1,1,1,1)


class UIObj_StartArrow(Widget):
    """
    @purpose UI Object class for States' visual representation
    """
    start = ObjectProperty(None)

    def __init__(self, **kwargs):
        """
        @purpose: Initialising some basic information about the Start Arrow
        """
        self.node = kwargs.get('node',0)
        self.origin_x = self.node.x+15
        self.origin_y = self.node.y+80
        super(UIObj_StartArrow,self).__init__(**kwargs)

        self.redraw(None)

    def redraw(self, node):
        """
        @purpose: Redraw the new Start Arrow
        """
        if node is not None:
            self.origin_x = node[0]+15
            self.origin_y = node[1]+80

        self.canvas.clear()
        self.canvas.add(Color(0,0,0))
        self.canvas.add(Line(bezier=(self.origin_x, self.origin_y, self.origin_x-50, self.origin_y+50), width=3))
        self.canvas.add(Triangle(points=(self.origin_x, self.origin_y, self.origin_x-20, self.origin_y,self.origin_x, self.origin_y+20)))


