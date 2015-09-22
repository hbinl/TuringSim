"""
@title FIT3140 Assignment 3 Spikes All in One Version
@description Spike test, contains Spike 1, 2, 3 and 4

            #######################################################
            To look for codes related to a particular spike,
            just find "Spike1", "#Spike2", "#Spike3" or "#Spike4"
            #######################################################

@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 1/9/2015
"""

# Kivy Dependencies
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
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
from kivy.clock import Clock

# Python Libraries
import os
import xml.etree.ElementTree as ET

# Team Spike Files
from ui_lib import *   #Spike2
from ui_dialog import *
from savetm_toxml import *   #Spike1
from machine_graph import SpikeMachine
from ui_container import Container


# KIVY HANDLING STUFF BELOW
class TuringSimApp(App):
    def build(self):
        return Container()

if __name__=="__main__":
    TuringSimApp().run()