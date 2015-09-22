"""
@title FIT3140 Assignment 3 Spikes - File dialog classes
@description Spike test, contains Spike 2, 3 and 4

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

# Python Libraries
import os
import xml.etree.ElementTree as ET

# Team Spike Files
from ui_lib import *   #Spike2
from ui_dialog import *
from savetm_toxml import *   #Spike1
from machine_graph import SpikeMachine


#Spike1
class Spike1Message(Widget):
    message = ObjectProperty(None)

    def test1(self):
        tree = create_newTM()
        # saving a brand new turing machine
        tree.write("1.xml")
        self.cancel_dialog()

    def test2(self):
        # update an existing Turing machine
        try:
            update_tm()
            self.cancel_dialog()
        except:
            self.cancel_dialog()

    def cancel_dialog(self):
        # used for dismissing the dialog box
        self.parent.parent.parent.dismiss()


#Spike3
class SaveFileChooserWindow(FloatLayout):
    """
    @purpose A FloatLayout for implementing Save file dialogs
    """
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = None

    def save_file(self, path, filename):
        # saving the path into this object for future use
        try:
            self.path = os.path.join(path)
            self.cancel_dialog()
        except ValueError:
            print("IndexError, os.path.join")

    def cancel_dialog(self):
        # used for dismissing the dialog box
        self.parent.parent.parent.dismiss()


#Spike2
class BrowseFileChooserWindow(FloatLayout):
    """
    @purpose A FloatLayout for implementing Load file dialogs
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = None

    def load_file(self, path, filename):
        # saving the path into this object for future use

        self.path = os.path.join(path,filename[0])
        self.cancel_dialog()
        # except:
        #     print("IndexError, os.path.join")

    def cancel_dialog(self):
        # used for dismissing the dialog box
        self.parent.parent.parent.dismiss()

class HomeScreenWindow(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = None

    def cancel_dialog(self):
        # used for dismissing the dialog box
        self.parent.parent.parent.dismiss()




