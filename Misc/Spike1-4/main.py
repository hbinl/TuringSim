"""
@title FIT3140 Assignment 3 Spikes
@description Spike test, contains Spike 1, 2, 3 and 4

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

from spike_ui_lib import *              #Spike2
from spike_dialog import *
from savetm_toxml import create_newTM   #Spike1


class Container(Widget):
    """
    @purpose Main container class, containing various general UI handlers
    """
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

        #Spike4
        self.zoomed = False
        Window.clearcolor = (0.7, 0.7, 0.7, 1)
        self.ids.layout_states.scale_max = 1.5
        self.ids.layout_states.scale_min = 0.1
        self.ids.layout_states.translation_touches = 2
        self.ids.layout_states.do_rotation = False

        #Spike3
        self.edit_mode = False

    ################## SPIKE 1 ###################

    #Spike1
    def savexml_handler(self, text):
        tree = create_newTM()  # saving a brand new turing machine
        tree.write("1.xml")

    ################## SPIKE 1 ###################

    def load_handler(self, text):
        self._popup = Popup(title="Load a Turing Machine XML File",
                            content=BrowseFileChooserWindow(),
                            size_hint=(0.85, 0.85))
        self._popup.bind(on_dismiss=self.after_load_handler)
        self._popup.open()

    def save_handler(self, text):
        self._popup = Popup(title="Save as a Turing Machine XML File",
                            content=SaveFileChooserWindow(),
                            size_hint=(0.85, 0.85))
        self._popup.bind(on_dismiss=self.after_save_handler)
        self._popup.open()

    def edit_handler(self, button):
        if button.text == "Done":
            button.text ="Edit"
            self.children[0].canvas.clear()
            self.remove_widget(self.children[0])
            self.edit_mode = False
        else:
            button.text = "Done"
            self.edit_mode = True

            bl = UIObj_Edit()
            self.add_widget(bl)

            anim = Animation(x=0, y=0, duration=0.2)
            anim.start(bl)

            bl.add_widget(UIObj_State_Template(id="State",
                                               x = 600,
                                               y = 10,
                                               size=(100,100)))
            bl.add_widget(UIObj_State_Halting_Template(id="Halt",
                                                       x=760,
                                                       y=10,
                                                       size =(100,100)))


    ################## SPIKE 4 ###################
    #Spike4
    def zoomplus_handler(self):
        if self.zoomed is False:
            self.zoomed = True
            mat = Matrix().scale(1.25, 1.25, 1.25)
            self.ids.layout_states.apply_transform(mat)

    #Spike4
    def zoomminus_handler(self):
        if self.zoomed is True:
            mat = Matrix().scale(0.8, 0.8, 0.8)
            self.ids.layout_states.apply_transform(mat)
            self.zoomed = False
    ################## SPIKE 4 ###################

    def after_save_handler(self, obj):
        #TODO : insert Spike 3 here
        if obj.content.path is not None:
            print obj.content.path


    def after_load_handler(self, obj):
        if obj.content.path is not None:
            self.zoomminus_handler()
            self.edit_mode = False
            board = self.ids.layout_states
            board.pos = (0,0)
            board.clear_widgets()

            i = 0
            win_x, win_y = Window.size
            start = 100
            state_size = 100
            padding = 80
            y_hint = 0.1
            state_size = 100
            transition_width = 2

            xml_tree = ET.parse(obj.content.path)
            xml_states = xml_tree.find("states")

            for child in xml_states:
                x_pos = start+(i*(state_size+padding))
                if x_pos > Window.size[0]:
                    i = 0
                    x_pos = start+(i*(state_size+padding))
                    y_hint += 0.1
                y_pos = win_y*y_hint

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
                transition = UIObj_Transition(tid=str(child.attrib["name"]),
                                              origin_x=x_pos+(state_size/2),origin_y=y_pos+(state_size/2),
                                              end_x=x_pos*2, end_y=y_pos*2,
                                              width=transition_width,
                                              curve_factor=25,
                                              is_self_state=False)
                #board.add_widget(transition)
                board.add_widget(state)
                i += 1


################# KIVY HANDLING STUFF BELOW ###################

class Spike2App(App):
    def build(self):
        return Container()

if __name__=="__main__":
    Spike2App().run()